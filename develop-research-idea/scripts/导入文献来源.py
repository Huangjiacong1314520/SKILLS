#!/usr/bin/env python3
"""把 CSV/TSV 文献导出增量导入中文主证据池并保持稳定编号。"""

from __future__ import annotations

import argparse
import csv
import os
import re
import tempfile
import unicodedata
from pathlib import Path


HEADERS = [
    "文献编号",
    "标题",
    "作者",
    "年份",
    "期刊",
    "DOI",
    "链接",
    "摘要",
    "关键词",
    "数据库记录号",
    "检索来源",
    "检索轮次",
    "导入文件",
    "证据层级",
    "纳入状态",
    "纳入或排除理由",
]


ALIASES = {
    "文献编号": ["文献编号", "id", "record id"],
    "标题": ["标题", "title", "document title", "article title"],
    "作者": ["作者", "authors", "author", "author full names"],
    "年份": ["年份", "year", "publication year", "published"],
    "期刊": ["期刊", "journal", "source title", "publication name"],
    "DOI": ["doi", "digital object identifier"],
    "链接": ["链接", "link", "url", "document url"],
    "摘要": ["摘要", "abstract"],
    "关键词": ["关键词", "keywords", "author keywords", "index keywords"],
    "数据库记录号": [
        "数据库记录号",
        "eid",
        "accession number",
        "ut (unique wos id)",
        "database record id",
    ],
    "证据层级": ["证据层级", "evidence level"],
    "纳入状态": ["纳入状态", "screening status"],
    "纳入或排除理由": ["纳入或排除理由", "screening reason"],
}


def normalized_header(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip().casefold()
    return re.sub(r"\s+", " ", value)


ALIAS_LOOKUP = {
    normalized_header(alias): canonical
    for canonical, aliases in ALIASES.items()
    for alias in aliases
}


def normalized_doi(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip().casefold()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    value = re.sub(r"^doi:\s*", "", value)
    return value.strip()


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(char for char in value if char.isalnum())


def record_key(record: dict[str, str]) -> str:
    doi = normalized_doi(record.get("DOI", ""))
    if doi:
        return f"doi:{doi}"
    title = normalized_title(record.get("标题", ""))
    return f"title:{title}" if title else ""


def merge_list_value(old: str, new: str) -> str:
    values = [item.strip() for item in (old or "").split(";") if item.strip()]
    for item in [item.strip() for item in (new or "").split(";") if item.strip()]:
        if item not in values:
            values.append(item)
    return "; ".join(values)


def read_text_with_fallback(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"无法识别文件编码：{path}")


def detect_delimiter(text: str, suffix: str) -> str:
    if suffix.casefold() == ".tsv":
        return "\t"
    sample = text[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        return ","


def read_export(path: Path) -> list[dict[str, str]]:
    text = read_text_with_fallback(path)
    delimiter = detect_delimiter(text, path.suffix)
    rows = list(csv.DictReader(text.splitlines(), delimiter=delimiter))
    if not rows:
        return []

    mapped_rows: list[dict[str, str]] = []
    for raw in rows:
        mapped = {header: "" for header in HEADERS}
        for raw_header, raw_value in raw.items():
            canonical = ALIAS_LOOKUP.get(normalized_header(raw_header or ""))
            if canonical:
                value = (raw_value or "").strip()
                if canonical == "关键词" and mapped[canonical] and value:
                    mapped[canonical] = merge_list_value(mapped[canonical], value)
                elif value:
                    mapped[canonical] = value
        if mapped["标题"] or mapped["DOI"]:
            mapped_rows.append(mapped)
    return mapped_rows


def read_pool(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            {header: (row.get(header) or "").strip() for header in HEADERS}
            for row in reader
            if (row.get("标题") or row.get("DOI") or "").strip()
        ]


def next_number(records: list[dict[str, str]]) -> int:
    numbers = []
    for record in records:
        match = re.fullmatch(r"RE(\d{3,})", record.get("文献编号", "").strip())
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def write_pool_atomic(path: Path, records: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix="文献来源表-", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(records)
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="增量导入文献来源并按 DOI/标题去重。")
    parser.add_argument("--workspace", required=True, help="研究构想工作区")
    parser.add_argument("--input", required=True, help="CSV 或 TSV 导出文件")
    parser.add_argument("--database", required=True, help="检索数据库名称")
    parser.add_argument("--query-id", required=True, help="检索轮次，如 Q001")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    input_path = Path(args.input).expanduser().resolve()
    pool_path = workspace / "文献来源表.csv"

    if input_path.suffix.casefold() not in {".csv", ".tsv", ".txt"}:
        raise SystemExit("当前确定性导入脚本支持 CSV、TSV 和分隔文本文件。")
    if not input_path.is_file():
        raise SystemExit(f"找不到导入文件：{input_path}")

    records = read_pool(pool_path)
    by_key = {key: record for record in records if (key := record_key(record))}
    imported = read_export(input_path)
    number = next_number(records)
    added = 0
    merged = 0
    skipped = 0

    for incoming in imported:
        incoming["检索来源"] = args.database.strip()
        incoming["检索轮次"] = args.query_id.strip()
        incoming["导入文件"] = input_path.name
        incoming["证据层级"] = incoming["证据层级"] or (
            "摘要" if incoming["摘要"] else "题录"
        )
        incoming["纳入状态"] = incoming["纳入状态"] or "待筛选"
        key = record_key(incoming)
        if not key:
            skipped += 1
            continue

        existing = by_key.get(key)
        if existing:
            for header in HEADERS:
                if header in {"文献编号", "检索来源", "检索轮次", "导入文件"}:
                    continue
                if not existing[header] and incoming[header]:
                    existing[header] = incoming[header]
            for header in ("检索来源", "检索轮次", "导入文件"):
                existing[header] = merge_list_value(existing[header], incoming[header])
            if existing["证据层级"] == "题录" and incoming["证据层级"] == "摘要":
                existing["证据层级"] = "摘要"
            merged += 1
            continue

        incoming["文献编号"] = f"RE{number:03d}"
        number += 1
        records.append(incoming)
        by_key[key] = incoming
        added += 1

    write_pool_atomic(pool_path, records)
    print(f"主证据池：{pool_path}")
    print(f"新增：{added}；合并重复：{merged}；跳过无标题和 DOI：{skipped}")
    print(f"当前记录总数：{len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
