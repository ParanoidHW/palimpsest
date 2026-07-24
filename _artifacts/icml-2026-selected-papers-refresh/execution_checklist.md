# ICML 2026 用户题单续作执行清单

状态取值仅使用：`pending`、`done`、`blocked`、`skipped-with-reason`。

## 任务与修订

- [done] 读取 `AGENTS.md`、`00_meta/research-knowledge-organization.md`、`ai-algorithm-survey`、`research-knowledge-publisher` 及强制契约。
- [done] 解析组织：domain=`02_model_systems/ICML/2026`；mode=`hybrid`；survey slug=`icml-2026-selected-papers`；process root=`_artifacts`；canonical owner=该 Survey 与各 Paper。
- [done] 盘点现有 12 篇正式 Paper、Survey、README、paper index、figure inventory。
- [done] 在 `synthesis.md` 顶部建立集中修订信息；旧 process manifest 未找到，记录稳定 migration issue `migration-legacy-survey-manifest-missing-icml2026-001` 与恢复尝试。
- [done] 完成前重读本清单；没有未分类项。

## Workflow 1：范围

- [done] 范围限定为用户现有 12 篇题单的增量刷新，优先恢复 SplAttN、Dual-Latent、Flex-Forcing、OmniFit 的 PDF/source/code；并复查 LIME、DODO、MTP Self-Distillation 的截断 source。
- [done] 记录纳入/排除、时间、venue 与 method/system-adoption 分桶。

## Workflow 2：当前检索

- [done] 记录 2026-07-24 的精确通用搜索查询与来源。
- [done] 覆盖 GitHub/维护列表、arXiv、OpenReview/ICML 官方 venue、作者/项目页。
- [done] 对 hybrid lane 记录模型、代码、配置、runtime/kernel adoption 与 evidence class。

## Workflow 3：影响信号

- [done] 刷新候选论文的引用、交叉引用、GitHub stars/forks/更新、代码采用和列表出现频次；所有易变指标带日期/来源；API rate-limit 项显式留空。

## Workflow 4：候选数据库

- [done] 创建/刷新 `paper_db.jsonl`，12 项去重且含 affiliations/evidence、repo/citation/cross-reference/list signals。
- [done] 创建/刷新 `system_db.jsonl`，method paper、technical report、native/optional/third-party adoption 分桶且身份稳定。

## Workflow 5：选择

- [done] 创建 `selection.md`，保留用户题单 12 项，明确优先修复的 4 篇与后续 source-only 刷新项、排除/venue mismatch 原因、机构分布和访问限制。

## Workflow 6：单篇深评

- [done] 完整读取 agent contract；计算 contract 与项目 `paper-deep-review` tree hash。
- [done] 建立 `agent_dispatch_log.md`；每篇一份不可修改 task packet、唯一 dispatch/runtime agent identity。
- [done] 共享工作区审计失败后，改用每篇独立 full Git clone 与 clone-local 完整 pre/post audit；该 remediation 已在 SplAttN 与 Flex-Forcing 通过。
- [done] SplAttN：完整 24-page PDF、完整 source、ICML poster 60900→Spotlight、official code commit、checkpoint metadata 均刷新；fresh agent revised review 通过 independent-clone audit 与父级验收。
- [blocked] Dual-Latent：已定位 OpenReview `SFWWUr9V7c`、原投稿 PDF 索引、ICML Spotlight 与声明的 GitHub；直接 PDF/API/attachment 均 Cloudflare 403，代码 URL 返回 404。agent 产出内部校验通过的 blocked revision，但父级因 out-of-root audit 失败判 `rejected`，不得 promotion。
- [done] Flex-Forcing：完整 PDF/source、项目/venue、两张原论文图已刷新；无官方 code/checkpoint；父级判 `accepted-with-limitations`。
- [blocked] OmniFit：精确身份恢复为 OpenReview `8RY20mLzup`、ICML Spotlight；PDF/source/API/code 仍不可得，单篇交付按 primary-PDF gate 判 rejected，仅提升身份与阻塞元数据。
- [done] MTP Self-Distillation：完整 source、官方 commit `167413e` 和 5 张图已由 fresh agent/父级验收；LiME/DODO 本轮未发现优先级高于已修复项的新 source/code 闭环。
- [done] 后续 dispatch 已切换到独立 clone；Dual-Latent 的共享工作区交付仍保持 rejected，未综合或 promotion。
- [done] 被接受论文的视觉证据均覆盖 mechanism 与 result/system；rejected/blocked 论文按 skip contract 记录；contact sheet 与逐图 100% QA 完成。
- [done] 被接受论文完成 problem → visual → mechanism → code/operator/kernel → evidence → limitation 闭环及 core-design rationale。
- [done] 父级合并 paper-local inventories；生成并检查 9 图 survey contact sheet；正式资产 promotion 后逐图复核。

## Workflow 7：综合

- [done] 创建 process `synthesis.md`，含范围、修订史、资源/影响、候选/机构、时间线、taxonomy、lineage、横向对比、术语符号、rationale、infra、趋势和证据局限。
- [done] 逐篇核心小节引用已接受 handoff/analysis；rejected 证据未写成既定技术结论。
- [done] 分开统计 confirmed ICML、preprint/workshop 与 adoption buckets。

## Workflow 8：文档驱动示意图

- [done] 检查 `OPENROUTER_ICU_API_KEY` 与 `$openrouter-icu-image`：key 可用，但安装的 CLI 仅支持 `generate`/`edit`。
- [skipped-with-reason] 不存在技能强制要求的 `responses-doc --input-file synthesis.md` 文档驱动入口；不以纯 prompt 图片替代。

## Publication

- [done] 创建并解析知识组织；确定 update 优先于 duplicate create。
- [done] 完成并 JSON/schema-validate `knowledge-promotion-plan.json` 和 `knowledge-change-set.json`；最终状态将在冻结前刷新。
- [done] 仅将稳定 Survey/Paper/Evidence/QA-passed Asset 提升到正式目录；PDF/source/render/crop/log/QA/manifest 留在 `_artifacts`。
- [done] 更新 README → Survey → Paper → Asset 正链与 Paper → Survey/README 反链。
- [done] 正式 Markdown 不引用 `_artifacts`、绝对路径、page render 或未跟踪资产。
- [done] 运行 publisher validator 并保存 `knowledge-validation.json`；当前 0 errors / 0 warnings，新增 MTP/Omni 修改后将再跑一次。

## Deliverable manifest 与冻结

- [done] 创建根 `deliverable_manifest.json`；论文 revision identity 与 manifests 一致。
- [done] Draft 2020-12 structural validation 通过且 errors 为空。
- [done] semantic validation 覆盖 artifact hashes、revision/history/latest、migration resolution、paper identity/count、agent uniqueness、manifest/dispatch、terminology/symbol、rationale、visual aggregation、frozen checklist；根状态因 unresolved migration 保持 blocked。
- [done] 冻结引用 artifacts 后重算 hashes、重跑结构与语义验证；后续变化必须新修订。

## Quality Checks

- [done] 必需全局 artifacts 齐全：search/github/impact/db/selection/dispatch/inventory/synthesis/manifest。
- [done] 搜索四类来源、hybrid entity lane、affiliations、impact signals 均有证据；受限/缺失项有分类。
- [done] 12 项角色明确；所有实际修订 paper 均由 fresh one-paper agent 使用项目 `paper-deep-review`。
- [blocked] Dual-Latent unique dispatch/provenance/artifact hashes 已核验；sequential audit 因不可归因的外部批量文件清理失败。
- [done] counted visual 的 caption、编号、PDF 页、page size、bbox、path、claim、report location、QA 字段齐全。
- [done] contact-sheet 初筛与每张 crop 原分辨率检查完成；每 crop 仅一个编号对象和完整 caption，无无关内容/过量留白。
- [done] 每张 counted visual 在 Paper/Survey 或正式 inventory 中链接并有分析；缺失 visual 有独立精确 skip evidence。
- [done] claim matrix、rationale、evidence loop、代码 commit/path、OpenReview cross-check 与 limitations 完成。
- [done] `synthesis.md` 的集中术语/符号、revision history 与 manifest 一致。
- [skipped-with-reason] 用户未请求 PPT/演示文稿，因此 presentation skill、deck 与 rendered QA 不适用。
- [done] 链接/锚点/资产存在性/Git tracking/孤立文档/孤立资产/forbidden references 全部通过。
- [done] 最终答复分别说明 research validation、publication validation、仍缺失的 PDF/source/code/paywall/网络或提取失败。
