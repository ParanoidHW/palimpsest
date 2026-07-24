# Search-index evidence transcription

> Evidence class: search-engine extraction of the public OpenReview original-submission attachment, accessed 2026-07-24. This is not a local PDF extraction. It is adequate only for qualified fact recovery and is not evidence that the final PDF, figures, reviews, rebuttal, or code were inspected.

## Identity and venue

- Forum: `https://openreview.net/forum?id=SFWWUr9V7c`
- Indexed original-submission attachment: `https://openreview.net/attachment?id=SFWWUr9V7c&name=originally_submitted_PDF`
- Forum index reports: published 2026-04-30; last modified 2026-06-24; ICML 2026 Spotlight; authors Hao-Xuan Ma, Jin-Fei Qi, YiCheng Xiao, Han-Jia Ye; submission number 18981; CC BY 4.0.
- ICML page: `https://icml.cc/virtual/2026/poster/63955`; cached locally as `../retrieval/icml-poster.html`.
- The indexed original-submission text is anonymous and labels itself preliminary/under review. Because no final PDF was acquired, material differences between that submission and the accepted version are unknown.

## Method facts recovered from indexed Sections 4.1–4.3

- Figure 2 is described as three lightweight additions to a frozen backbone: dual latent memories, a memory injector, and a discrete router.
- The two learned, input-agnostic latent banks are
  \[
  Z^{(s)}\in\mathbb{R}^{M_s\times d},\quad s\in\{v,r\}.
  \]
- For budget \(k\in\mathcal K_+\), the injector contextualizes the selected prefix of the chosen bank:
  \[
  M_t=g_\phi(E_t,Z^{(s)}_{1:k},k)\in\mathbb{R}^{k\times d}.
  \]
- The injector is described as LoRA integrated into a replica of the frozen base MLLM. Context embeddings are projected into injector width, concatenated with latent vectors, processed, and the last \(k\) states projected back to backbone width.
- Injection is eligible only when the generated prefix ends with a delimiter pattern in a small set \(\mathcal D\), and a per-sample cap \(N_{\max}\) bounds routed injections.
- At an eligible step, the router action is
  \[
  a_t=(s_t,k_t),\quad s_t\in\{v,r\},\ k_t\in\mathcal K_+.
  \]
- The router is described as a LoRA-augmented head that reuses the latest final-layer hidden state. Training samples actions; inference uses greedy action selection.
- Stage 1 pre-warms the two latent banks with visual and reasoning teacher representations using within-branch cosine alignment, a cross-teacher hinge term with margin \(m\), and a separation term between the two banks.
- Stage 2 trains the injector and both latent banks while the router is disabled, exposes mixed memory types and budgets, and uses either supervised next-token likelihood or GRPO; a weak specialization-preservation term is retained.
- Stage 3 freezes injector and memories and trains the router with GRPO:
  \[
  \max_\psi\ \mathbb E_{\tau\sim\pi_\psi}[R_{\rm task}(\tau)+\lambda_{\rm eff}R_{\rm eff}(\tau)]
  -\beta\,{\rm KL}(\pi_\psi\Vert\pi_{\rm ref}).
  \]
  Indexed appendix prose says efficiency reward favors smaller average injection budgets and is counted only for correct answers.

## Experimental facts recovered from indexed Tables 1–4

### Main results, Table 1

- Backbones: Qwen2.5-VL-7B and InternVL-3-8B.
- General benchmarks: MMVet, MMStar, RealWorldQA. Reasoning benchmarks: MMMU, MathVerse, MathVision, MathVista.
- Qwen2.5-VL-7B:
  - SFT baseline general average 65.62; DLMR-SFT 71.45.
  - GRPO baseline reasoning average 50.29; DLMR-RL 56.45.
  - DLMR-SFT reasoning average 53.84.
- InternVL-3-8B:
  - SFT baseline general average 73.37; DLMR-SFT 79.25.
  - GRPO baseline reasoning average 54.33; DLMR-RL 63.08.
- These are complete-method comparisons, not per-component attribution.

### Injector ablation, Table 2

- Qwen2.5-VL-7B, four reasoning benchmarks:
  - frozen injector average 50.44;
  - trainable injector average 53.84.
- This is direct evidence that the learned contextualization interface matters under the reported setup, but it does not isolate injector architecture choices.

### Disentanglement ablation

- Indexed prose reports shared single memory average 47.53 versus dual memory 53.84, an absolute gain of 6.31.
- MathVision is reported as 26.68 versus 35.32, an absolute gain of 8.64.
- This directly supports separating the two banks relative to the tested shared-memory replacement, but does not independently verify that the learned banks store exactly the semantics assigned to them.

### Router/budget ablation, Table 4

| Variant | Reasoning average accuracy | Average generated tokens |
|---|---:|---:|
| fixed \(k=4\), no router | 51.55 | 664 |
| fixed \(k=8\), no router | 52.71 | 732 |
| fixed \(k=16\), no router | 52.04 | 765 |
| adaptive DLMR router | 53.84 | 677 |

- Versus the best fixed-accuracy setting \(k=8\), adaptive routing is +1.13 accuracy points and -55 tokens (-7.51%).
- Versus \(k=16\), it is +1.80 accuracy points and -88 tokens (-11.50%).
- Versus \(k=4\), it is +2.29 accuracy points but +13 tokens (+1.96%).
- Therefore Table 4 supports a better reported accuracy–token frontier than the tested fixed-budget choices; it does not by itself prove lower latency or fewer tokens than the vanilla backbone.
- Figure 4 text says the best budget cap differs by task family: general tasks peak at \(k_{\max}=16\), reasoning tasks at \(k_{\max}=32\).

## Training-data fact recovered

- Indexed prose says both backbones use the same training dataset across the three stages, including training splits of selected benchmarks when available plus OpenMMReasoner; benchmarks without a training split are evaluation-only.
- Dataset filtering, exact sample counts, leakage controls, hyperparameters, hardware, precision, and seeds were not recoverable without the PDF appendix or code.

## Evidence boundary

- No numbered figure/table image is available for crop QA.
- No review note IDs, review scores, rebuttal text, or meta-review body were recoverable.
- No code path, commit, model checkpoint, or configuration was available.
- Search-index extraction can omit layout, superscripts, equation operators, rows, appendix qualifications, or revisions. Every claim based on this file remains qualified accordingly.
