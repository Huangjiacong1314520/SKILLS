# 来源覆盖

本文件只做规则—来源—所有者映射，不重复工作流。来源文件不是运行时依赖；Skill 分享给其他用户后仍可独立使用。

## 来源类别

- **[原] 搜聚分思想**：`搜聚分思想笔记.md` 及其中定位的《科研论连载-1》《科研论连载-2》与钓鱼法材料。
- **[训] 训练营实践**：`AI研究论文选题开题训练营/提示词.md` 的第 1、2、3、3.2、3.3、4 集。
- **[Agent] 工程适配**：本 Skill 的可靠性与协作设计；参考 `AI Coding for Real Engineering` 的“我现在应该从哪里进入”“主流程”“上下文与资产的生命周期”“HITL、AFK 与自动化边界”，以及 Matt Skills 的公开说明。

## 公开工程参考

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [grilling](https://github.com/mattpocock/skills/tree/main/skills/grilling)
- [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/domain-modeling)
- [grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/grill-with-docs)
- [research](https://github.com/mattpocock/skills/tree/main/skills/research)
- [wayfinder](https://github.com/mattpocock/skills/tree/main/skills/wayfinder)
- [handoff](https://github.com/mattpocock/skills/tree/main/skills/handoff)
- [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/writing-great-skills)

## 规则映射

| 规则组 | 类别与定位 | 唯一所有者 |
| --- | --- | --- |
| 输出控制阅读；材料足够即行动 | [原] `少读文献，但达到有效的输出`、`无输出不学习`、`只要能吃饱` | `SKILL.md` |
| 可回退、增量补充、失败作为反馈 | [原] `每一个操作都可以随时返回后退`、`验合` | `SKILL.md` |
| 钓鱼法、鲸吞法及真实结果回流 | [原] `搜`；[训] 第 1 集检索式迭代 | `SEARCH.md` |
| 同一任务材料归拢、稳定编号与追溯 | [原] `聚`；[训] 第 2 集文献预处理 | `SKILL.md`、`LITERATURE-ANALYSIS.md` |
| 目标驱动分组、交叉组合、能启动即暂停 | [原] `分` | `SKILL.md` |
| 分批逐篇分析与跨批元分析 | [训] 第 3 集 `指令一`、`指令二` | `LITERATURE-ANALYSIS.md` |
| 阶段报告人工审阅，防止创意被平均 | [训] 第 3 集 `寻宝式审阅技巧` | `LITERATURE-ANALYSIS.md` |
| 候选标题、科学问题、路线、创新价值、立论依据 | [训] 第 3 集课题提案模板 | `CANDIDATE-VIEWS.md` |
| 高创新、高可行性与结构化创新视角 | [训] 第 3.2、3.3 集 | `CANDIDATE-VIEWS.md` |
| 选定后回到完整文献池定向筛选与深化 | [训] 第 4 集 | `HANDOFF.md` |
| 题录/摘要/全文证据深度 | [Agent] 可靠性设计 | `LITERATURE-ANALYSIS.md` |
| 动态技术批次、三种逻辑职责 | [Agent] 工具容量与职责隔离 | `LITERATURE-ANALYSIS.md` |
| 主模式/少数信号双通道与去向 | [训] 人工审阅动机；[Agent] 记录结构 | `LITERATURE-ANALYSIS.md` |
| 主视角生成—对照视角审查 | [训] 生成视角；[Agent] 对照审查 | `CANDIDATE-VIEWS.md` |
| 三个固定决策门与一次一个决定 | [Agent] `grilling` 适配 | `SKILL.md` |
| 确认的术语和长期边界在下一次追问前进入领域文档 | [Agent] `grilling` + `domain-modeling` 适配 | `SKILL.md` |
| 最小状态、单一事实源、唯一阻塞前沿 | [Agent] 工程资产生命周期适配 | `SKILL.md`、`COLLABORATION.md` |
| 数据库接力检索—检索回传包 | [Agent] 受限访问适配 | `SEARCH.md` |
| 选题交接包、全文门与交接状态 | [原] 选题到“验”的边界；[Agent] 交接契约 | `HANDOFF.md` |
| 手动进入 `validate-research-idea` | [Agent] 用户调用边界 | `SKILL.md` |

## 明确不归源的设计

以下内容只标为 **[Agent]**：固定三个决策门、证据深度分层、动态批次、三种逻辑职责、双通道去向、候选对照审查、状态目录、数据库回传格式、全文交接门。不得把它们写成“搜聚分原文规定”或“训练营明确要求”。
