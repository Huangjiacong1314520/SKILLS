# 个人科研工作流 Skills

这是一个面向 Codex 的个人科研工作流 Skill 仓库，包含论文推导共创、研究构想发展、迭代检索、手写笔记转 Markdown、执行规格整理、论文审查和研究构想验证等能力。

参考的是国家杰青钟老师的[科研论内容]([《科研论》首页](https://www.keyanlun.com/))。搜聚分验合五步法，后续补充合。

## Skills

| Skill | 用途 |
| --- | --- |
| `checklist` | 【checklist】对论文手稿与证据进行结构化审查 |
| `derive-paper-with-user` | 与用户分段讨论、确认并共创论文推导 |
| `develop-research-idea` | 【搜聚分】基于真实文献和证据池发展研究候选 |
| `fishing-search` | 【搜.钓鱼法】将模糊主题转化为反馈驱动的迭代搜索 |
| `handwritten-notes-to-markdown` | 将手写笔记和公式图片转写为 Markdown |
| `to-execution-spec` | 将对话、草稿或计划整理为执行规格 |
| `validate-research-idea` | 【验】为研究创新点设计最短验证闭环 |

## 兼容性与安装

这些目录遵循 Codex Skill 约定：每个 Skill 至少包含 `SKILL.md`，可选的 `agents/openai.yaml`、`scripts/`、`references/` 和 `assets/` 按需提供。将所需 Skill 目录复制到 Codex 的 skills 目录，或在支持的环境中将本仓库作为 Skill 集合加载；具体安装位置取决于宿主版本和本地配置。

显式调用示例：

```text
使用 $fishing-search 帮我把这个模糊主题变成可执行的文献检索循环。
使用 $to-execution-spec 将刚才的讨论保存为执行规格。
```

部分 Skill 依赖联网检索、用户提供的材料或其他已安装的 Skill。缺少依赖时应采用各 Skill 中说明的降级方式，不应假设本仓库包含外部服务。

## 目录结构

每个 Skill 的主入口是 `SKILL.md`。详细规则、脚本和素材放在对应目录的 `references/`、`scripts/`、`assets/` 中；仓库级说明不放入单个 Skill 目录，以保持 Skill 的渐进式加载结构。

## 第三方内容与许可证

本仓库的 MIT 许可只适用于维护者原创且维护者有权授权的代码、指令和文档。`THIRD_PARTY_NOTICES.md` 所列的第三方材料不因仓库根目录的 MIT 文件而获得重新授权。

仓库中部分 `references/source/` 文件含有来自第三方平台的文章或较长摘录。公开分发前，请确认版权和再发布许可；在确认前，不要将这些文件视为 MIT 内容，也不要把它们复制到其他公开仓库。由于仓库过去可能已经公开，新增提交中的删除不会清除 Git 历史中的旧版本。

## 贡献

提交改动前，请保持 Skill 名称与目录一致、frontmatter 仅包含必需字段，并运行 `skill-creator` 提供的 `quick_validate.py`。新增外部材料时请同时补充来源、许可和必要的归属说明。

## License

见 [`LICENSE`](LICENSE) 和 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
