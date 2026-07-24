# Agent Dispatch Log

## Batch

- Task: `icml-2026-selected-papers-refresh`
- Isolation mode: `sequential-audit`
- Shared workspace: `/mnt/d/huangwei/markdown`
- Contract: `.agents/skills/ai-algorithm-survey/references/paper-review-agent-contract.md`
- Contract SHA-256: `4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32`
- Required skill directory: `.agents/skills/paper-deep-review`
- Required skill tree SHA-256: `a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd` (sorted relative-path `sha256sum` manifest; the initially recorded absolute-path-derived hash was invalid)

## `dispatch-dual-latent-refresh-20260724`

- Paper key: `2026_dual-latent-memory-routing`
- Requested agent task name: `dual_latent_refresh`
- Runtime agent id/canonical task: `/root/dual_latent_refresh`
- Spawn mode: `fork_turns="none"`
- Task packet: `papers/2026_dual-latent-memory-routing/task_packet.yaml`
- Task packet SHA-256: `87c3524e225af0585d6d0f63fff572260bacfa1329e5b55526147d930b8dccfa`
- Allowed write root: `papers/2026_dual-latent-memory-routing`
- Filesystem isolation: shared workspace, fresh sequential agent, complete outside-root pre/post path+SHA-256 audit excluding `.git/`
- Pre-dispatch audit: `/tmp/icml-dual-pre.sha256`, 1,547 files, digest `51660de4d293f6f1a28024be4b1998c3ffd67f8d9a0e42a90788d706bec6a351`
- Agent completion/handoff: agent stopped before substantive work; no handoff/review artifacts created
- Task/skill/contract recheck: task and contract matched; required skill tree failed (`packet 98a41917...`, correct `a338c821...`)
- Artifact manifest verification: not applicable; agent correctly created no delivery
- External state comparison: failed; task packet unchanged, but 3,158 unrelated files were removed and 13 files changed outside the allowed root during the interval, chiefly under pre-existing `_artifacts/output/`; `.interaction-recorder-state.json` also changed. These changes were not made by this dispatch and are not reconciled as agent-owned changes.
- Parent verdict: `rejected`
- Failed checks/remediation/user approval: provenance mismatch alone requires rejection. Parent corrected the relative-path skill-tree hash and will issue a new dispatch; no rejected evidence is used.

## `dispatch-dual-latent-refresh-r2-20260724`

- Paper key: `2026_dual-latent-memory-routing`
- Requested agent task name: `dual_latent_refresh_r2`
- Runtime agent id/canonical task: `/root/dual_latent_refresh_r2`
- Spawn mode: `fork_turns="none"`
- Task packet: `papers/2026_dual-latent-memory-routing/task_packet.yaml`
- Task packet SHA-256: `82ac3acc063511cbbb2f577b1eb17857884a4b8947c115c06dcab1a13378972c`
- Allowed write root: `papers/2026_dual-latent-memory-routing`
- Filesystem isolation: shared workspace, fresh sequential agent, complete outside-root pre/post path+SHA-256 audit excluding `.git/`
- Pre-dispatch audit: original `/tmp/icml-dual-r2-pre.sha256`; finalization sub-window `/tmp/icml-dual-r2-finalize-pre.sha256`. The repository's unrelated process-artifact population changed repeatedly while no parent write occurred.
- Agent completion/handoff: agent reported blocked delivery `1.1.0`, revision `rev-refresh-r2-20260724`; `agent_handoff.md` exists.
- Task/skill/contract recheck: task packet `82ac3acc...` unchanged; skill tree `a338c821...`, contract `4dc80bfb...`, and prior manifest `4371334a...` matched.
- Artifact manifest verification: agent reported 14 covered files and `sha256sum -c` pass; parent must still reject because write-boundary audit failed.
- External state comparison: failed. In the bounded finalization interval, 4,472 files outside `allowed_write_root` disappeared and 4 changed. Removed paths are dominated by unrelated pre-existing `_artifacts/output/ai_algorithm_survey_diffusion/**`; changed paths include `.interaction-recorder-state.json`, `.obsidian/workspace.json`, and two unrelated formal/asset paths. The agent denied out-of-root edits, but this shared workspace provides no enforced sandbox and the changes cannot be attributed deterministically.
- Parent verdict: `rejected`
- Failed checks/remediation/user approval: complete out-of-root integrity check failed, which is an unconditional rejection branch. Internally valid blocked artifacts are retained only as process evidence and must not be synthesized or promoted. Further shared-workspace dispatch is paused pending an enforced independent worktree/sandbox or explicit user acceptance of a reduced isolation standard.

## `dispatch-splattn-refresh-20260724`

- Paper key: `2026_splattn`
- Requested agent task name: `splattn_refresh`
- Runtime agent id/canonical task: `/root/splattn_refresh`
- Spawn mode: `fork_turns="none"`
- Task packet: `/tmp/icml-splattn-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_splattn/task_packet.yaml`
- Task packet SHA-256: `c360805cfc20ff1495f77a865f6cc13aaf75ba662ff590395a845e27d8865779`
- Allowed write root: `/tmp/icml-splattn-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_splattn`
- Filesystem isolation: independent full Git clone `/tmp/icml-splattn-agent-work`; clone-local complete outside-root pre/post path+SHA-256 audit excluding clone `.git/`; main-repository artifact GC is outside this work copy.
- Prior manifest: main-repository same-paper delivery `1006a623...`
- Pre-dispatch audit: `/tmp/icml-splattn-pre.sha256`, 1,509 files, digest `12cca3a833deb58e56f38f6602e1808ec62218dc6e1d3cb062f0bdf8758598f0`
- Agent completion/handoff: complete; `agent_handoff.md`, version `1.1.0`, revision `rev-splattn-refresh-20260724`
- Task/skill/contract recheck: task packet `c360805c...` unchanged; skill tree `a338c821...`, contract `4dc80bfb...`, prior manifest `1006a623...` matched
- Artifact manifest verification: 168 files passed `sha256sum -c`; manifest digest `18281c4eadf62f06eabaccfe3ad13aa0525b9ca0712796e3b91b4f0436bb2ae4`
- External state comparison: passed; post manifest exactly equals pre manifest (1,509 paths and digest `12cca3a...`)
- Parent verdict: `accepted`
- Failed checks/remediation/user approval: none. Parent independently validated schema/semantics and inspected contact sheet plus Figure 1/Figure 8 crops at original resolution; both visual types passed.

## `dispatch-flex-forcing-refresh-20260724`

- Paper key: `2026_flex-forcing`
- Requested agent task name: `flex_forcing_refresh`
- Runtime agent id/canonical task: `/root/flex_forcing_refresh`
- Spawn mode: `fork_turns="none"`
- Task packet: `/tmp/icml-flex-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_flex-forcing/task_packet.yaml`
- Task packet SHA-256: `23b8b44214240a7a6b5156da50e93136b2065219f3b829dcaad2bf68f1034409`
- Allowed write root: `/tmp/icml-flex-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_flex-forcing`
- Filesystem isolation: independent full Git clone `/tmp/icml-flex-agent-work`; clone-local complete outside-root pre/post audit excluding clone `.git/`
- Prior manifest: `075d43a...`
- Pre-dispatch audit: `/tmp/icml-flex-pre.sha256`, 1,509 files
- Agent completion/handoff: complete; version `1.0.0`, revision `rev-source-complete-20260724`
- Task/skill/contract recheck: task `23b8b442...`, skill tree `a338c821...`, contract `4dc80bfb...`, prior manifest `075d43a8...` all matched
- Artifact manifest verification: 65 files passed; manifest digest `9fc75663fa0be093eb2aebec0efcf513ea8bd09e72a8b5916280651c36f2f91c`
- External state comparison: passed after path-normalized clone-local comparison; the first parent comparison used relative pre paths versus absolute post paths and was discarded as a comparison-method error
- Parent verdict: `accepted-with-limitations`
- Failed checks/remediation/user approval: OpenReview reviews/rebuttal and direct poster snapshot were blocked by challenge/403; Spotlight venue was triangulated from official NVIDIA, ICML Downloads, accepted source and indexed OpenReview metadata. No official code/checkpoint exists. Parent inspected contact sheet and both final crops at original resolution; all passed.

## `dispatch-omnifit-refresh-20260724`

- Paper key: `2026_omnifit-layer-compression`
- Requested agent task name: `omnifit_refresh`
- Runtime agent id/canonical task: `/root/omnifit_refresh`
- Spawn mode: `fork_turns="none"`
- Task packet: `/tmp/icml-omnifit-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_omnifit-layer-compression/task_packet.yaml`
- Task packet SHA-256: `2f66791214f44280e322cd2488065266aa7c3c4cd2242dbe92eeeedb13fda155`
- Allowed write root: `/tmp/icml-omnifit-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_omnifit-layer-compression`
- Filesystem isolation: independent full Git clone `/tmp/icml-omnifit-agent-work`; clone-local complete outside-root pre/post audit excluding clone `.git/`
- Prior manifest: `c1e005ec...`
- Pre-dispatch audit: `/tmp/icml-omnifit-pre.sha256`, 1,509 files
- Agent completion/handoff: blocked delivery; version `1.1.0`, revision `rev-omnifit-openreview-refresh`
- Task/skill/contract recheck: task `2f667912...`, skill tree `a338c821...`, contract `4dc80bfb...`, prior manifest `c1e005ec...` all matched
- Artifact manifest verification: all 10 covered files passed; digest `b51944a5c3987a97ffc0a44433ac962db7e0a203d6c0c905184616d9c59cbe74`
- External state comparison: passed after relative-path clone-local comparison
- Parent verdict: `rejected`
- Failed checks/remediation/user approval: primary PDF/source was unavailable, which is an unconditional rejection branch for technical synthesis/promotion. Parent independently promoted only stable identity/venue/access-blocker metadata from OpenReview `8RY20mLzup` and ICML poster `65962`; no agent-derived technical claims or visuals were promoted.

## `dispatch-mtp-self-distillation-refresh-20260724`

- Paper key: `2026_multi-token-self-distillation`
- Requested agent task name: `mtp_self_distillation_refresh`
- Runtime agent id/canonical task: `/root/mtp_self_distillation_refresh`
- Spawn mode: `fork_turns="none"`
- Task packet: `/tmp/icml-mtp-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_multi-token-self-distillation/task_packet.yaml`
- Task packet SHA-256: `d6d97797e906ad66911e3e54836c73971b6eadd895ded85a7fe8448ba3cfd4ea`
- Allowed write root: `/tmp/icml-mtp-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_multi-token-self-distillation`
- Filesystem isolation: independent full Git clone with complete outside-root pre/post hash audit
- Prior manifest: `f8e8b9b439ca7db62ff8c98df1f630f94cd617ef8a12963b689a899a1420e1c6`
- Pre-dispatch audit: `/tmp/icml-mtp-pre.sha256`, 1,509 files
- Agent completion/handoff: complete; version `1.1.0`, revision `rev-mtp-source-code-refresh`
- Task/skill/contract recheck: task, skill tree, contract and prior manifest all matched
- Artifact manifest verification: 251 files passed; digest `0d27b047ff8c9d4d26b4cfe9301a30831d625e5cfd93876233396dbb35dea4f0`
- External state comparison: passed exactly
- Parent verdict: `accepted-with-limitations`
- Failed checks/remediation/user approval: OpenReview absent and per-checkpoint HF metadata not completely frozen. Parent inspected the contact sheet and all five crops at original resolution; Figure 12 was newly recropped with complete caption and promoted.
