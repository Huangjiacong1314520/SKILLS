#!/usr/bin/env python3
"""校验研究工作区结构、主池编号和候选引用。"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path


REQUIRED_FILES = [
    "研究简报.md",
    "检索日志.md",
    "文献来源表.csv",
    "证据笔记.md",
    "关系分析.md",
    "候选研究构想.md",
]

REQUIRED_HEADERS = [
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


def normalized_doi(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip().casefold()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return re.sub(r"^doi:\s*", "", value).strip()


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(char for char in value if char.isalnum())


def read_pool(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验研究构想工作区。")
    parser.add_argument("--workspace", required=True, help="研究构想工作区")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not workspace.is_dir():
        raise SystemExit(f"找不到工作区：{workspace}")

    for filename in REQUIRED_FILES:
        if not (workspace / filename).is_file():
            errors.append(f"缺少文件：{filename}")

    pool_path = workspace / "文献来源表.csv"
    source_ids: set[str] = set()
    if pool_path.is_file():
        headers, records = read_pool(pool_path)
        missing_headers = [header for header in REQUIRED_HEADERS if header not in headers]
        if missing_headers:
            errors.append("文献来源表缺少字段：" + "、".join(missing_headers))

        seen_ids: set[str] = set()
        seen_keys: dict[str, str] = {}
        for line_number, record in enumerate(records, start=2):
            if not any((value or "").strip() for value in record.values()):
                continue
            source_id = (record.get("文献编号") or "").strip()
            if not re.fullmatch(r"RE\d{3,}", source_id):
                errors.append(f"第 {line_number} 行文献编号无效：{source_id or '空'}")
            elif source_id in seen_ids:
                errors.append(f"文献编号重复：{source_id}")
            else:
                seen_ids.add(source_id)
                source_ids.add(source_id)

            doi = normalized_doi(record.get("DOI", ""))
            title = normalized_title(record.get("标题", ""))
            key = f"doi:{doi}" if doi else (f"title:{title}" if title else "")
            if key and key in seen_keys:
                errors.append(
                    f"疑似重复来源：{seen_keys[key]} 与 {source_id or f'第{line_number}行'}"
                )
            elif key:
                seen_keys[key] = source_id or f"第{line_number}行"

            if not (record.get("检索来源") or "").strip():
                warnings.append(f"{source_id or f'第{line_number}行'}缺少检索来源")
            if (record.get("证据层级") or "").strip() not in {"题录", "摘要", "全文"}:
                warnings.append(f"{source_id or f'第{line_number}行'}的证据层级未规范")

    brief_path = workspace / "研究简报.md"
    if brief_path.is_file():
        brief = brief_path.read_text(encoding="utf-8")
        for heading in ("## 启动诊断", "## 当前状态", "## 状态变更记录"):
            if heading not in brief:
                errors.append(f"研究简报缺少章节：{heading}")

    candidates_path = workspace / "候选研究构想.md"
    if candidates_path.is_file():
        text = candidates_path.read_text(encoding="utf-8")
        cited_ids = set(re.findall(r"\bRE\d{3,}\b", text))
        for missing in sorted(cited_ids - source_ids):
            errors.append(f"候选文件引用了主池中不存在的文献：{missing}")

        sections = re.split(r"(?=^### 候选\d+\s*$)", text, flags=re.MULTILINE)
        for section in sections:
            match = re.search(r"^### (候选\d+)\s*$", section, flags=re.MULTILINE)
            if not match:
                continue
            candidate_id = match.group(1)
            status = re.search(
                r"^- 证据状态：(初步候选|证据化候选)\s*$",
                section,
                flags=re.MULTILINE,
            )
            if status and not re.search(r"\bRE\d{3,}\b", section):
                errors.append(f"{candidate_id}是{status.group(1)}，但没有引用文献编号")

    for warning in warnings:
        print(f"[警告] {warning}")
    for error in errors:
        print(f"[错误] {error}")

    if errors:
        print(f"校验失败：{len(errors)} 个错误，{len(warnings)} 个警告")
        return 1

    print(f"校验通过：{workspace}（{len(warnings)} 个警告）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
