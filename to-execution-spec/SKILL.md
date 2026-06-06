---
name: to-execution-spec
description: Turns a long conversation, draft, or plan into a formal execution spec for implementation. Use when the user wants to convert discussion context into a saved Markdown execution specification, especially for refactors, research workflows, technical plans, interface contracts, or implementation-ready designs.
---

# To Execution Spec

Create a concise but implementation-ready execution spec from the current conversation or a user-provided draft. The output is not a PRD, ADR, issue list, or code implementation.

## Default Output

- Save a Markdown file under `docs/execution-specs/`.
- Use a Chinese filename by default: `<主题>执行规格.md`.
- Also reply with the saved path and a short summary.
- If the user asks for chat-only output, do not save a file.
- If the target file already exists, do not overwrite unless the user explicitly asked to update it; otherwise ask whether to update or create a versioned file.

## Inputs

Use one of these modes:

1. Current conversation plus lightweight project context.
2. A user-specified draft, plan, document, or file plus lightweight project context.

Before writing, do lightweight exploration only:

- Read `CONTEXT.md` if present and use its terminology.
- Read relevant ADRs if present, but do not create ADRs.
- Read relevant docs and user-mentioned files.
- Inspect stable project structure and key entry points when useful.
- Do not modify code, create issues, run broad tests, install dependencies, or perform deep repo exploration unless separately requested.

## Decision Rules

- Only put user-confirmed decisions, user-proposed decisions, or clearly inherited project facts into "已定决策".
- Do not promote assistant suggestions that the user did not confirm.
- If a decision is useful but unconfirmed, put it in "待定与暂缓问题" or ask before generating.
- If unresolved questions block first-version implementation, list them as "未解决阻塞项" and ask at most 3 focused questions before writing.
- If unresolved questions do not block the first version, keep them in "待定与暂缓问题".
- Do not update `CONTEXT.md`; this skill only reads it.
- Do not create ADRs, issues, tasks, or code.
- Avoid User Stories and product PRD language unless the user explicitly asks for a PRD.

## Required Structure

Use this template for complex work. Remove empty sections for small tasks only.

```markdown
# <主题>执行规格

## 1. 目标

## 2. 非目标

## 3. 第一版范围

## 4. 背景与现状

## 5. 已定架构

## 6. 接口契约

## 7. 关键设计决策

## 8. 实现顺序

## 9. 验收标准

## 10. 待定与暂缓问题

## 11. 参考资料
```

## Section Guidance

- **目标**: State the concrete outcome the implementation should achieve.
- **非目标**: Explicitly exclude scope that would cause first-version bloat.
- **第一版范围**: Define what is enough for the first executable version.
- **背景与现状**: Summarize current repo state, legacy assets, documents, and constraints.
- **已定架构**: Describe agreed structure and module boundaries.
- **接口契约**: This section is mandatory. Define inputs, outputs, data shapes, visibility boundaries, and forbidden dependencies.
- **关键设计决策**: Explain why key choices were made and which alternatives were rejected.
- **实现顺序**: Order steps by dependency. Each step should say what to do, why it comes now, and what becomes verifiable.
- **验收标准**: Write natural, observable acceptance criteria. Check behavior, interface boundaries, experiment loops, outputs, and failure cases. Do not merely check that files or functions exist.
- **待定与暂缓问题**: Include only non-blocking follow-up topics. Blocking questions must be separated before writing.
- **参考资料**: List sources used, such as `CONTEXT.md`, ADRs, docs, papers, and relevant source files. The spec body must still be self-contained; do not use "see chat history" as a substitute for decisions.

## Interface Examples

Small code-shaped examples are allowed when they clarify contracts:

```matlab
result = method.run(sim_data, method_cfg);
```

Do not include full implementations.

## Final Self-Check

Before saving, check internally that:

- Confirmed decisions are not mixed with unconfirmed suggestions.
- Terms match `CONTEXT.md` when available.
- Interface contracts are explicit.
- Pending items do not block first-version execution.
- Acceptance criteria are observable and not file-existence busywork.
- The document avoids User Stories and product PRD tone.
- The body is self-contained and includes references.
