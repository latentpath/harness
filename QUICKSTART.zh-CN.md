## 中文快速使用

Harness 是放在**项目本地**的 AI 工程工作流。它不负责替代 IDE、CLI Agent 或模型，而是让不同 Agent 按相同的工程阶段、artifact 和 approval contract 工作。

### 1. 初始化项目

先正常创建项目，例如 Flutter：

```bash
flutter create my_app
cd my_app
```

然后将对应 Harness pack **完整、干净地复制**到项目中：

```text
my_app/
├── harness/
├── lib/
├── test/
└── ...
```

不要修改 `harness/AGENTS.md` 来保存项目自己的技术偏好。

### 2. 建立项目级工程约束（推荐）

如果项目有长期技术决策，例如：

* Flutter 使用 Riverpod；
* UI 不直接访问 API；
* repository 负责外部数据访问；
* 某些依赖或架构模式被固定或禁止；

复制：

```text
harness/templates/project-constitution.md
```

填写后保存为项目根目录：

```text
AGENTS.md
```

形成：

```text
project/
├── AGENTS.md          # 项目级工程约束
├── harness/
│   └── AGENTS.md      # Harness workflow contract
└── ...
```

只填写已经确定的工程决策。

不要因为模板存在，就提前冻结尚未需要的 networking、routing、persistence 等技术选择。

### 3. 从真实需求开始一个 Task

为每个独立工程变更选择稳定的 task id，例如：

```text
add-login-flow
add-item-list
add-logout-flow
```

给 Agent 原始需求，然后只执行 SPEC：

```text
Read the project `AGENTS.md` if present and `harness/AGENTS.md`, and follow the installed Harness.

Task ID: `add-login-flow`

Raw requirement:

<你的真实需求>

Execute only the SPEC phase. Stop when the SPEC phase is complete, or when the Harness requires `BLOCKED` or `NEEDS_REVISION`.
```

SPEC 的职责是形成：

```text
harness/work/<task-id>/spec.md
```

`spec.md` 是该 task 的 normative requirement truth。

如果缺少关键事实，例如外部 API contract，正确结果可以是：

```text
BLOCKED
```

不要让 Agent 根据惯例猜测未知 contract。

取得 authoritative information 后，重新执行 SPEC，解除 blocker。

### 4. PLAN

SPEC 完整且没有 blocker 后，建议新开 Agent 会话：

```text
Read the project `AGENTS.md` if present and `harness/AGENTS.md`, and follow the installed Harness.

Task ID: `<task-id>`

Execute only the PLAN phase according to the Harness. Stop when the PLAN phase is complete, or when the Harness requires `BLOCKED` or `NEEDS_REVISION`.
```

Agent 会读取 repository、SPEC 和项目约束，并生成：

```text
harness/work/<task-id>/plan.md
```

PLAN 可以决定如何实现，但不能弱化 SPEC。

### 5. 人工批准 PLAN

检查 `plan.md`。

确认可以执行后计算 SHA-256：

```bash
sha256sum harness/work/<task-id>/plan.md
```

创建：

```text
harness/work/<task-id>/approval.json
```

例如：

```json
{
  "status": "approved",
  "plan_sha256": "<plan.md SHA-256>",
  "approved_at": "<ISO-8601 timestamp>",
  "approved_by": "human"
}
```

然后运行 Harness 提供的 approval checker。
如：bash harness/scripts/check-approval.sh add-login-flow

批准后不要再修改 `plan.md`。

如果 PLAN 改变，必须重新计算 hash 并重新批准。

### 6. IMPLEMENT

建议新开 Agent 会话：

```text
Read the project `AGENTS.md` if present and `harness/AGENTS.md`, and follow the installed Harness.

Task ID: `<task-id>`

Verify the task's approval, then execute only the IMPLEMENT phase according to the Harness. Stop when the IMPLEMENT phase is complete, or when the Harness requires `BLOCKED`, `NEEDS_REVISION`, or `FAILED`.
```

IMPLEMENT 负责：

```text
source changes
tests
development.md
validation.status
validation.log
```

成功完成 IMPLEMENT 的状态是：

```text
COMPLETED
```

不是 `APPROVED`。

最终批准权属于 REVIEW。

### 7. REVIEW

再次新开 Agent 会话：

```text
Read the project `AGENTS.md` if present and `harness/AGENTS.md`, and follow the installed Harness.

Task ID: `<task-id>`

Execute only the REVIEW phase according to the Harness. Stop when the REVIEW phase is complete, or when the Harness requires `BLOCKED`, `NEEDS_REVISION`, or `FAILED`.
```

REVIEW 应独立检查：

```text
SPEC
↓
approved PLAN
↓
actual implementation
↓
machine validation evidence
↓
development narrative
```

最终 verdict 由 REVIEW 独占，例如：

```text
APPROVED
CHANGES_REQUESTED
```

### 8. 日常使用原则

Harness 不要求所有阶段使用同一个 Agent 或同一个模型。

例如可以使用：

```text
VS Code Copilot
Kilo CLI
其他能够读取 repository 并修改文件的 Agent
```

关键不是 conversation history，而是项目中的 artifacts。

因此推荐在主要阶段之间新开会话，验证：

```text
repository + Harness + artifacts
```

本身是否足以完成 handoff。

模型选择也不必固定为最高档。普通 task 可以使用默认模型；遇到复杂 ambiguity、architecture trade-off、连续失败、跨领域重构或高风险问题时，再升级到更强 reasoning model。

### 最小工作流

日常使用时只需要记住：

```text
raw requirement
      ↓
SPEC
      ↓
PLAN
      ↓
human approval
      ↓
IMPLEMENT
      ↓
validation
      ↓
REVIEW
```

Harness 的目标不是让 AI 写更多代码，而是让 AI 的工程变更具备明确的需求真相、执行授权、机器证据和独立审查。
