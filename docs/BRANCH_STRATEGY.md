# Branch Strategy

## 目标

为 `py313-monorepo-starter` 提供可执行且可复核的分支管理策略，确保本地开发、代码评审、CI 验证与发布行为一致。

## 分支模型

- `main`: 唯一长期分支，始终保持可发布状态。
- `feat/<topic>`: 新功能开发分支，来源于 `main`，通过 PR 合并回 `main`。
- `fix/<topic>`: 缺陷修复分支，来源于 `main`，通过 PR 合并回 `main`。
- `chore/<topic>`: 工具链、依赖、脚本或配置维护分支。
- `docs/<topic>`: 文档变更分支。
- `hotfix/<topic>`: 线上紧急修复分支，修复后立即回合并 `main` 并打补丁标签。
- `release/<version>`: 预发布收敛分支（可选），用于冻结版本并做最终验证。

分支命名仅使用小写字母、数字与短横线，`<topic>` 建议用动宾结构，例如 `feat/add-health-endpoint`。

## 保护规则（建议在 GitHub Branch Protection 落地）

- 禁止直接 push 到 `main`，必须通过 Pull Request。
- `main` 至少 1 名 Reviewer Approve 后才允许合并。
- 必须通过必需检查：`lint-type-test`（见 `.github/workflows/python313-ci.yml`）。
- 要求分支与 `main` 同步（Require branches to be up to date）。
- 禁止强推（force push）与删除受保护分支。

## 合并策略

- 默认使用 `Squash and merge`，保持 `main` 历史清晰。
- 提交信息建议遵循 Conventional Commits（如 `feat: ...`、`fix: ...`、`docs: ...`）。
- PR 必须包含变更说明、验证结果与风险评估。

## 发布策略

- 采用语义化版本标签：`vMAJOR.MINOR.PATCH`，示例：`v0.1.0`。
- 正常发布流程：
  1. 在 `main` 完成版本收敛；
  2. 确认 CI 全绿；
  3. 创建并推送标签；
  4. 生成 Release Notes（可自动或手工）。
- 紧急修复流程：
  1. 从 `main` 切 `hotfix/*`；
  2. 修复并通过 CI；
  3. PR 合并回 `main`；
  4. 打 `vX.Y.(Z+1)` 标签。

## 例外与追溯

- 若因平台权限问题无法完成远端动作（如无法触发 CI 或受限于凭据），需在 `docs/EVIDENCE_LOG.md` 记录：
  - 执行时间；
  - 执行命令；
  - 原始错误信息；
  - 可替代验证结果（本地同构检查、配置静态校验等）。
