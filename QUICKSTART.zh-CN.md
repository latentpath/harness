# 项目 Harness 使用流程

## 0. 先理解 Harness

Harness 不是 Agent Runtime，也不是为了规定每一行代码应该怎么写。它提供repository-local 工作流，把：

``` text
Prompt → Plausible Code
```

转变成：

``` text
Goal → Contract → Approved Plan → Implementation → Evidence → Review
```

### 0.1 核心层级

``` text
Project
└── Phase
    └── Task
```

-   **Project**：长期项目目标、架构和工程规则。
-   **Phase**：当前阶段允许做什么、禁止做什么、何时完成。
-   **Task**：一个边界明确、可独立验收的具体需求。

不要用一个 Task 一次实现整个 Phase。例如 Product Catalog Phase 可以拆成
`create-product`、`get-product`、`list-products`。

### 0.2 一个 Task 的生命周期

``` text
Raw Requirement
      ↓
     SPEC
      ↓
     PLAN
      ↓
 Human Approval
      ↓
  IMPLEMENT
      ↓
   VALIDATE
      ↓
    REVIEW
```

权威关系是 `SPEC > PLAN`。PLAN 不能削弱、删除或重新解释 SPEC。

### 0.3 Human 与 Agent 的职责边界

Harness 的目标不是让 Human 遥控 Agent写代码，而是建立清晰的**授权边界**。

Human 主要负责：

-   明确 Task 要解决什么和什么不做；
-   审查 SPEC 是否准确表达需求；
-   审查 PLAN 是否处于可接受的授权边界；
-   批准 SPEC + PLAN；
-   判断 material deviation 是否需要重新批准；
-   接受或拒绝最终 REVIEW。

Agent / Model 主要负责：

-   检查 repository reality；
-   在批准边界内选择具体实现方式；
-   编码、测试和调试；
-   运行 validation；
-   产生可审计 evidence。

> **约束 What、Why、Boundary、Acceptance；授权 How。**

不要为了控制 Agent 而提前规定不必要的类名、方法名、文件位置或实现细节。

## 1. 5 分钟开始一个 Task

对于已经安装好 Harness 的 repository，通常只需要准备：

``` text
Task ID
Governing phase
Raw requirement
```

例如：

``` text
Task ID: get-product
Governing phase: docs/phases/phase-1.md

Raw requirement:
Implement GET /api/products/{productId}.
...
```

### 1.1 从 SPEC 开始

给 SPEC Agent：

``` text
Read the project root `AGENTS.md`, `harness/AGENTS.md`, and the governing
phase definition.

Task ID: `get-product`
Governing phase: `docs/phases/phase-1.md`

Raw requirement:

<当前任务的具体 requirement>

Execute only SPEC according to `harness/prompts/01-spec.md`.
Record the governing phase path in SPEC Repository Context.
Stop after COMPLETED, BLOCKED, or NEEDS_REVISION.
```

Agent 应首先运行：

``` bash
python3 harness/scripts/harnessctl.py stage-start get-product spec
```

该命令会校验 Task ID、自动创建 `harness/work/get-product/` 并记录 SPEC
baseline。

**不要手工创建 Task 目录。**

### 1.2 按阶段推进

``` text
SPEC
→ Human 检查
→ PLAN
→ Human 检查
→ Human Approval
→ IMPLEMENT + VALIDATE
→ REVIEW
```

每个 Agent
只执行指定阶段，达到该阶段终止状态后停止，不自行进入下一阶段。

### 1.3 最重要的完成规则

``` text
IMPLEMENT COMPLETED ≠ Task APPROVED
Validation PASS     ≠ Task APPROVED
```

`BUILD SUCCESS` 和 validation PASS 只证明机器检查通过。**只有 REVIEW
可以给出最终 `APPROVED`。**

## 2. 核心文件与概念

### 2.1 项目根目录 `AGENTS.md`

回答"这个项目长期应该如何建设？"。它保存项目目标、技术栈、架构边界、持久化和事务原则、测试规则、禁止事项、Phase
治理制度等长期稳定规则。

不要在根目录 `AGENTS.md` 中记录当前 Active Phase 或 Task 状态。

### 2.2 `harness/AGENTS.md`

回答"AI Agent 应当按照什么工作流执行任务？"。它定义
SPEC、PLAN、APPROVAL、IMPLEMENT、VALIDATE 和 REVIEW
的规则。不要把项目特有技术决策写入该文件。

### 2.3 `docs/phases/phase-N.md`

回答"当前项目阶段允许做什么、禁止做什么、何时结束？"。Governing phase
至少应明确 Phase Goal、Allowed / Blocked scope、Phase Constraints 和
Phase Success Criteria。不能使用未填写的模板作为 governing phase。

### 2.4 Raw Requirement

回答"这一个 Task 具体需要交付什么行为？"。Requirement
应定义目标、输入、输出、失败行为、非目标和可观察验收结果，但不应指定未经
repository 检查的类名、文件名或具体实现方案。

### 2.5 `spec.md`

SPEC Agent 综合：

``` text
Project AGENTS.md
+ Harness AGENTS.md
+ governing phase
+ Raw requirement
+ repository reality
→ spec.md
```

SPEC 是当前 Task
的规范合同，主要定义必须成立的行为和边界，不应过早固定属于 PLAN
的实现选择。

### 2.6 `plan.md`

PLAN 在已完成 SPEC 和实际 repository
基础上提出实现策略。它应明确关键技术决策、modification
surface、数据与错误处理策略、测试策略以及必要风险，同时给 implementation
mechanics 留出合理自主空间。

## 3. 完整 Task 生命周期

### 3.1 SPEC

SPEC Agent 应读取项目和 Harness 规则、governing phase、Raw requirement
与必要 repository facts；运行 `stage-start`；生成 `spec.md`；执行
ownership 检查；更新 `state.json`；然后停止。

SPEC 不应修改业务源码、测试、migration、`pom.xml` 或配置，也不应创建
PLAN 或开始实现。

典型产物：

``` text
.spec-baseline.json
spec.md
state.json
```

### 3.2 PLAN

PLAN Agent 读取 SPEC 和 repository，输出：

``` text
.plan-baseline.json
plan.md
state.json
```

PLAN 不修改实现代码、不自行批准、不改变 SPEC。完成后由 Human 审查。

### 3.3 Human Approval

Human 接受 SPEC 和 PLAN 后，`approval.json` 同时绑定两者的 SHA-256：

``` json
{
  "status": "approved",
  "spec_sha256": "<spec sha256>",
  "plan_sha256": "<plan sha256>",
  "approved_at": "2026-08-30T05:35:00Z",
  "approved_by": "<approver>"
}
```

检查：

``` bash
sha256sum harness/work/<task-id>/spec.md harness/work/<task-id>/plan.md
TASK_ID=<task-id> bash harness/scripts/check-approval.sh
```

SPEC 或 PLAN 在批准后发生变化，旧 approval 不再授权新的内容，IMPLEMENT必须停止并重新进入正确治理流程。

#### Approval 时间戳与 chronology

`approved_at` 使用 ISO-8601 UTC；`Z` 表示 UTC。每一次新的 Human Approval / re-approval 都必须记录**真实批准时间**，不能沿用上一次 approval 的timestamp。

Git 可能显示本地时间和 UTC offset。例如 `2026-08-30 13:35:00 +0800` 与`2026-08-30T05:35:00Z` 可以表示同一时刻。检查 chronology时应先统一时区。

``` text
Approval hash
→ 证明批准了什么

Approval timestamp + Git history
→ 帮助证明何时批准
```

### 3.4 IMPLEMENT

IMPLEMENT Agent 验证 approval，按 SPEC 和 approved PLAN 实现，添加必要测试，运行 validation，生成或更新 `development.md`，执行ownership 检查并更新 state。

IMPLEMENT 不得修改：

``` text
spec.md
plan.md
approval.json
review.md
```

IMPLEMENT 可以报告 `COMPLETED`，不能报告 `APPROVED`。如果 validation 失败，应留在 IMPLEMENT 解决或明确报告失败。

### 3.5 VALIDATE

正式 Task 使用：

``` bash
TASK_ID=<task-id> bash harness/scripts/validate.sh
```

典型 evidence：

``` text
validation.log
validation.status
validation.json
metrics.json
```

机器 evidence 优先于 Agent 的文字陈述。但是 Machine PASS
只证明机器检查通过，不证明 implementation
已被最终接受。测试全绿仍可能存在 SPEC 偏差、PLAN 未授权修改、Phase scope
violation 或配置/治理问题。

### 3.6 REVIEW

REVIEW 独立检查：

``` text
governing phase
→ SPEC
→ approved PLAN
→ actual implementation
→ machine validation evidence
→ development narrative
→ Git / workflow evidence（必要时）
```

输出：

``` text
.review-baseline.json
review.md
state.json
```

REVIEW 独占最终 verdict：

``` text
APPROVED
CHANGES_REQUESTED
```

REVIEW 不应因为 `BUILD SUCCESS` 就自动批准。

## 4. Change Control 与 Reconciliation

### 4.1 Implementation 本身不符合已批准的 SPEC / PLAN

例如 contract、validation、persistence 或已批准方案没有正确实现：

``` text
REVIEW
→ CHANGES_REQUESTED
→ IMPLEMENT 修正
→ fresh VALIDATION
→ REVIEW
```

### 4.2 Implementation 合理，但超出 approved PLAN

如果 Agent 为解决真实技术问题进行了 material repository change，而该 change 没有被当前 PLAN 授权，不要仅仅事后修改 PLAN 来"解释"已经发生的 deviation。

正确流程：

``` text
REVIEW
→ CHANGES_REQUESTED
→ PLAN amendment
→ Human re-approval
→ IMPLEMENT reconciliation
→ fresh VALIDATION
→ REVIEW
```

> **PLAN amendment 是新的授权，不是对历史 deviation 的洗白。**

Human 必须真实检查 amended PLAN，并产生新的 approval binding 和真实的
`approved_at`。

### 4.3 IMPLEMENT reconciliation 不等于重写实现

如果现有 implementation 已符合 amended + re-approved
PLAN，不需要为了走流程而重复编码。

Reconciliation 可以是：

1.  验证当前 approval；
2.  验证现有 implementation 符合 amended PLAN；
3.  `stage-start implement`；
4.  不做不必要的代码修改；
5.  重新运行 validation；
6.  `stage-check implement`；
7.  恢复 `implement / COMPLETED`；
8.  产生新的 evidence；
9.  再进入 REVIEW。

核心顺序：

``` text
新的授权
→ 授权后的 IMPLEMENT reconciliation
→ 授权后的 fresh evidence
→ independent REVIEW
```

## 5. Evidence、State 与 Git

### 5.1 Task artifacts

``` text
harness/work/<task-id>/
├── .spec-baseline.json
├── .plan-baseline.json
├── .implement-baseline.json
├── .review-baseline.json
├── spec.md
├── plan.md
├── approval.json
├── state.json
├── development.md
├── validation.log
├── validation.status
├── validation.json
├── metrics.json
└── review.md
```

这些文件由对应 stage 或 Harness 工具产生。不要提前创建空 artifact、跨 stage 修改其他 stage 拥有的
artifact，或为了让当前状态"看起来正确"而改写历史 evidence。

### 5.2 `state.json`

`state.json` 表示当前 workflow state，而不是永久历史日志。常见状态：

``` text
BLOCKED
NEEDS_REVISION
FAILED
COMPLETED
APPROVED
CHANGES_REQUESTED
ABORTED
```

应确保它与当前实际 stage 一致。

### 5.3 Git 是 workflow 的审计记录

Harness artifacts 描述当前合同、授权和 evidence；Git history 提供重要
chronology。

> **Git history 是 Harness workflow 的行车记录仪。**

建议在重要 checkpoint 形成清晰 commit，例如绿色 baseline、accepted SPEC
/ PLAN、Human approval / re-approval、implementation
checkpoint、reconciliation evidence、final REVIEW。

不要求为每个微小动作单独 commit，但不要把整个 lifecycle 压成一个无法恢复 chronology 的大 commit。Cold-start Reviewer 在需要时应能结合 artifact content、hashes、timestamps 和 Git history 重建关键治理顺序。

## 6. 常见冲突与正确处理

  -----------------------------------------------------------------------
  情况                                正确处理
  ----------------------------------- -----------------------------------
  缺少关键业务/API 决策               `BLOCKED` 或 `NEEDS_REVISION`

  Requirement 越过 Phase Gate         返回 Requirement / SPEC

  PLAN 与 SPEC 冲突                   返回 PLAN

  SPEC 本身错误                       返回 SPEC

  approval 后 SPEC/PLAN 改变          停止 IMPLEMENT，重新批准

  validation 失败                     留在 IMPLEMENT

  REVIEW 发现实现错误                 返回 IMPLEMENT

  REVIEW 发现合理但未授权的 PLAN      PLAN amendment → re-approval →
  deviation                           reconciliation

  re-approval                         使用真实的新 `approved_at`

  validation PASS                     仍需 REVIEW

  Agent 想顺手做非 Task 工作          不做，除非重新授权
  -----------------------------------------------------------------------

## 7. 常见错误

### 7.1 手工创建 Task 目录

不要：

``` bash
mkdir -p harness/work/<task-id>
```

使用：

``` bash
python3 harness/scripts/harnessctl.py stage-start <task-id> <stage>
```

### 7.2 一个 Agent 连续跑多个未经授权的 stage

如果提示词要求 `SPEC only`，SPEC 完成后必须停止。同理适用于 PLAN、IMPLEMENT 和 REVIEW。

### 7.3 把 SPEC 写成 implementation plan

SPEC 应描述合同、边界和acceptance。具体数据库机制、类结构、helper、framework mechanics 通常属于
PLAN 或 IMPLEMENT。

### 7.4 PLAN 过细或过虚

过细会变成 Human 遥控 Agent 写代码；过虚则没有明确授权边界。PLAN 应明确 material decisions 和 modification surface，同时授权合理 implementation detail。

### 7.5 把 validation PASS 当作最终批准

正确关系：

``` text
BUILD SUCCESS
→ REVIEW
→ APPROVED / CHANGES_REQUESTED
```

### 7.6 事后修改 PLAN 给 deviation 洗白

合理但未经授权的 material deviation 应走：

``` text
PLAN amendment
→ Human re-approval
→ reconciliation
→ validation
→ review
```

### 7.7 re-approval 沿用旧 timestamp

新的批准必须记录新的**真实批准时间**。

### 7.8 只相信 Agent 的总结

``` text
repository reality > Agent narrative
machine evidence    > Agent claim
```

## 8. 项目首次安装与初始化

本节只用于第一次把 Harness 引入项目。已经安装好的 repository 可以跳过。

### 8.1 项目基线

当前项目采用 Java 21、Spring Boot 4.1.1、Spring MVC、Spring Data JPA、PostgreSQL、Flyway 和 Maven Wrapper。

只有 repository 中实际存在的配置和依赖才属于 repository fact。项目基本法或 Phase 中提到的技术方向，不代表对应依赖已经安装。缺失依赖应由具体 Task 的 PLAN 提出、说明并经过 Human Approval 后添加。

### 8.2 安装 Harness

将 Spring Boot Harness pack 的**内容**复制到项目根目录的 `harness/`：

``` text
project/
├── AGENTS.md
├── pom.xml
├── src/
├── docs/
└── harness/
    ├── AGENTS.md
    ├── README.md
    ├── prompts/
    ├── scripts/
    ├── templates/
    └── work/
```

正确路径是 `project/harness/AGENTS.md`，不要安装成 `project/harness/spring-boot/AGENTS.md`。

### 8.3 创建项目基本法

``` bash
cp harness/templates/project-constitution.md AGENTS.md
```

填写长期稳定的项目规则，不记录当前任务状态。

### 8.4 创建 Phase

``` bash
mkdir -p docs/phases
cp harness/templates/phase.md docs/phases/phase-1.md
```

完整填写 Phase Goal、Allowed / Blocked scope、Constraints 和 Success Criteria。

### 8.5 配置项目和测试环境

根据项目需要配置 `pom.xml`、`application.yml`、专用非生产测试数据库及必要环境变量或 test profile。不要把不存在的 dependency 当作 repository fact。

### 8.6 建立绿色 baseline

``` bash
bash harness/scripts/self-check.sh
./mvnw clean verify
```

预期：

``` text
SELF-CHECK PASS
BUILD SUCCESS
```

然后提交：

``` bash
git add .
git commit -m "chore: establish harness experiment baseline"
```

后续 Task 从绿色 repository baseline 开始。

## 9. 日常 Checklist

### 开始 Task 前

-   [ ] 当前 Git baseline 是绿色的；
-   [ ] `bash harness/scripts/self-check.sh` 通过；
-   [ ] `./mvnw clean verify` 通过；
-   [ ] Task ID 唯一且稳定；
-   [ ] governing phase 已填写，不是空模板；
-   [ ] Raw requirement 描述的是一个 Task，而不是整个 Phase；
-   [ ] Requirement 没有越过 Phase Gate；
-   [ ] 没有手工创建 `harness/work/<task-id>/`。

### SPEC / PLAN 后

-   [ ] Agent 只执行了指定 stage；
-   [ ] ownership 检查通过；
-   [ ] `state.json` 与实际 stage 一致；
-   [ ] SPEC 没有不必要的 implementation leakage；
-   [ ] PLAN 没有削弱 SPEC；
-   [ ] PLAN 明确 material decisions，但没有遥控具体代码；
-   [ ] Human 已实际检查产物。

### Approval 时

-   [ ] SPEC hash 正确；
-   [ ] PLAN hash 正确；
-   [ ] `approved_at` 是本次真实批准时间；
-   [ ] timestamp 时区明确；
-   [ ] `check-approval.sh` PASS。

### IMPLEMENT 后

-   [ ] 没有修改 SPEC / PLAN / approval / review；
-   [ ] implementation 在 approved boundary 内；
-   [ ] validation evidence 是本轮 implementation/reconciliation
    后新产生的；
-   [ ] validation PASS；
-   [ ] `state.json` 正确。

### REVIEW 后

-   [ ] Reviewer 独立检查 SPEC、approved PLAN、actual implementation 和
    evidence；
-   [ ] material deviation 已被识别；
-   [ ] verdict 是 `APPROVED` 或 `CHANGES_REQUESTED`；
-   [ ] `APPROVED` 后形成清晰 Git checkpoint。

## 10. 一页式心智模型

``` text
Project AGENTS.md
    = 长期基本法

Phase
    = 当前阶段的范围与 Gate

Raw Requirement
    = 这一个 Task 的具体意图

SPEC
    = 必须满足的合同

PLAN
    = Human 批准的实现策略与授权边界

Approval
    = SPEC + PLAN 的内容绑定与批准证据

Implementation
    = Agent 在授权边界内自主完成 How

Validation
    = 机器证据，不等于最终批准

Review
    = 独立验收，独占最终 verdict

Git history
    = workflow chronology / 行车记录仪
```

> Human 确定方向、边界和验收标准。Agent / Model
> 在批准边界内自主解决实现细节。Harness
> 负责让偏差可发现、失败可恢复、交接有依据、结果可审计。
