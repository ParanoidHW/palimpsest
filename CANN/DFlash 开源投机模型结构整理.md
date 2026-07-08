更新时间：2026-05-29

## 结论摘要

截至 2026-05-29，DFlash README 中列出的 draft 模型里，能匿名读取 `config.json` 的公开模型显示出一个非常一致的规律：

- 公开版 draft 主体基本都不是目标模型家族各自的原生骨干，而是统一使用 `architectures = ["DFlashDraftModel"]`
- `model_type` 基本统一写成 `qwen3`
- 主体是一个小型 decoder-only draft stack，通常只有 4 到 8 层
- attention 主要分为两类：
  - `full_attention`
  - `sliding_attention`
- 头类型是 GQA 风格，即 `num_key_value_heads < num_attention_heads`
- 大多数模型的 `head_dim = 128`，公开可查里 `gpt-oss` 家族为 `head_dim = 64`
- `block_size` 多数为 16，但也有 8 或 10

## 源码级结构

根据 `dflash/model.py`，DFlash draft 的公开实现是统一的 `Qwen3DFlashAttention + Qwen3DFlashDecoderLayer + DFlashDraftModel` 结构。

### 1. 主体骨干

- `DFlashDraftModel` 继承自 `Qwen3PreTrainedModel`
- `layers = nn.ModuleList([Qwen3DFlashDecoderLayer(...)])`
- 每层由：
  - `self_attn = Qwen3DFlashAttention`
  - `mlp = Qwen3MLP`
  - `input_layernorm = Qwen3RMSNorm`
  - `post_attention_layernorm = Qwen3RMSNorm`
- 额外有一个 `fc`，把多个 target hidden states 拼接后映射回 `hidden_size`

### 2. Attention 类型

源码里 `Qwen3DFlashAttention` 的关键点：

- `self.is_causal = False`
  - 也就是 draft attention 本身是非因果的
- 位置编码使用 `Qwen3RotaryEmbedding`
- Q/K 使用 per-head `RMSNorm`
  - `q_norm = Qwen3RMSNorm(self.head_dim, ...)`
  - `k_norm = Qwen3RMSNorm(self.head_dim, ...)`
- Q 来自当前 draft/noise hidden states
- K/V 来自两部分拼接：
  - `target_hidden`
  - `hidden_states`
- 当某层 `layer_types[layer_idx] == "sliding_attention"` 时，使用 `sliding_window`
- attention kernel 并不固定死在 eager 上：
  - 默认 `eager_attention_forward`
  - 如果 `config._attn_implementation != "eager"`，则从 `ALL_ATTENTION_FUNCTIONS` 里切换

这说明 DFlash 的 draft attention 不是普通的“只看自身 prefix 的 causal self-attention”，而是：

- 非因果
- 带 RoPE
- 带 Q/K norm
- 对 `target_hidden + noise hidden` 联合做 attention
- 可按层切换为 full attention 或 sliding-window attention

### 3. 需要注意的规格解释

- `head_dim` 以 config 显式字段为准
- 不能简单用 `hidden_size / num_attention_heads` 反推 `head_dim`
- `num_attention_heads` 与 `num_key_value_heads` 不相等，说明公开 draft 采用的是 GQA/MQA 风格的 K/V 共享

## 公开可核实模型规格

下表来自匿名可访问的 Hugging Face `config.json`。

| 模型                                    | draft层数 | hidden_size | intermediate_size | num_attention_heads | num_key_value_heads | head_dim | attention 类型         | sliding_window | block_size |
| ------------------------------------- | ------: | ----------: | ----------------: | ------------------: | ------------------: | -------: | -------------------- | -------------: | ---------: |
| Qwen3.5-4B-DFlash                     |       5 |        2560 |              9728 |                  32 |                   8 |      128 | full x5              |              - |         16 |
| Qwen3-4B-DFlash-b16                   |       5 |        2560 |              9728 |                  32 |                   8 |      128 | full x5              |              - |         16 |
| Qwen3.5-9B-DFlash                     |       5 |        4096 |             12288 |                  32 |                   8 |      128 | full x5              |              - |         16 |
| Qwen3-8B-DFlash-b16                   |       5 |        4096 |             12288 |                  32 |                   8 |      128 | full x5              |              - |         16 |
| LLaMA3.1-8B-Instruct-DFlash-UltraChat |       5 |        4096 |             12288 |                  32 |                   8 |      128 | full x5              |              - |         10 |
| Qwen3.5-27B-DFlash                    |       5 |        5120 |             17408 |                  32 |                   8 |      128 | full x5              |              - |         16 |
| Qwen3.5-35B-A3B-DFlash                |       8 |        2048 |              6144 |                  32 |                   4 |      128 | full x8              |              - |         16 |
| Qwen3.6-35B-A3B-DFlash                |       8 |        2048 |              6144 |                  32 |                   4 |      128 | full x8              |              - |         16 |
| Qwen3-Coder-30B-A3B-DFlash            |       8 |        2048 |              6144 |                  32 |                   4 |      128 | full x8              |              - |         16 |
| Qwen3-Coder-Next-DFlash               |       8 |        2048 |              6144 |                  32 |                   4 |      128 | full x8              |              - |         16 |
| Qwen3.5-122B-A10B-DFlash              |       4 |        3072 |              9216 |                  32 |                   4 |      128 | sliding x3 + full x1 |           2048 |         16 |
| gemma-4-26B-A4B-it-DFlash             |       5 |        2816 |              5632 |                  32 |                   8 |      128 | sliding x4 + full x1 |           2048 |         16 |
| gemma-4-31B-it-DFlash                 |       5 |        5376 |             10752 |                  64 |                   8 |      128 | sliding x4 + full x1 |           2048 |         16 |
| gpt-oss-20b-DFlash                    |       8 |        2880 |              7680 |                  64 |                   8 |       64 | full x8              |              - |          8 |
| gpt-oss-120b-DFlash                   |       8 |        2880 |              7680 |                  64 |                   8 |       64 | full x8              |              - |         10 |
| Kimi-K2.5-DFlash                      |       6 |        7168 |             18432 |                  64 |                   8 |      128 | full x6              |              - |          8 |

## 按家族观察

### Qwen3 / Qwen3.5 / Qwen3.6 / Qwen3-Coder

- 基本都走 `qwen3` 型统一 draft 骨干
- 普遍使用 `head_dim = 128`
- 主要有两档：
  - 5 层 draft，`32 / 8 / 128`
  - 8 层 draft，`32 / 4 / 128`
- `Qwen3.5-122B-A10B-DFlash` 是当前公开表里最明显的 SWA 版本之一：
  - 4 层
  - 前 3 层 `sliding_attention`
  - 最后一层 `full_attention`
  - `sliding_window = 2048`

### Gemma-4

- 公开配置同样写成 `model_type = "qwen3"`
- 也走统一 DFlash draft 主体
- 都带 SWA：
  - 前 4 层 `sliding_attention`
  - 最后一层 `full_attention`
  - `sliding_window = 2048`
- `gemma-4-31B-it-DFlash` 的 heads 更大：
  - `num_attention_heads = 64`
  - `num_key_value_heads = 8`
  - `head_dim = 128`

### gpt-oss

- 和其他家族最明显的区别是 `head_dim = 64`
- `gpt-oss-20b-DFlash`:
  - 8 层
  - `64 / 8 / 64`
  - `block_size = 8`
- `gpt-oss-120b-DFlash`:
  - 8 层
  - `64 / 8 / 64`
  - `block_size = 10`

### Kimi

- 当前匿名可核实的是 `Kimi-K2.5-DFlash`
- 规格：
  - 6 层
  - `hidden_size = 7168`
  - `intermediate_size = 18432`
  - `64 / 8 / 128`
  - `full_attention x6`
  - `block_size = 8`

## 当前无法匿名核实的模型

截至 2026-05-29，下列模型页面存在 gated access，匿名请求 `config.json` 返回的是访问受限提示，因此这里不对其具体结构做猜测：

- `z-lab/Qwen3.6-27B-DFlash`
- `z-lab/Kimi-K2.6-DFlash`
- `z-lab/MiniMax-M2.5-DFlash`
- `z-lab/MiniMax-M2.7-DFlash`

## 总结

如果只回答“DFlash 现在开源的投机模型主体都是什么结构”，最准确的说法是：

- 它公开出来的 draft 主体基本是统一的 `DFlashDraftModel`
- 该 draft 模型在实现上是一个 `Qwen3` 风格的小型 decoder-only backbone
- attention 是非因果 attention，不是普通 causal self-attention
- 位置编码使用 RoPE
- Q/K 带 RMSNorm
- K/V 来自 `target_hidden` 与 `hidden_states` 的拼接
- 头组织上是 GQA 风格
- attention 层类型按模型不同可分为：
  - 全 full attention
  - 前若干层 sliding attention，最后一层或少数层 full attention

如果只看公开可查模型，最常见规格可以概括为：

- 4 到 8 层 draft
- `head_dim` 以 128 为主
- `num_attention_heads / num_key_value_heads` 常见为：
  - `32 / 8`
  - `32 / 4`
  - `64 / 8`
- `block_size` 常见为：
  - 16
  - 10
  - 8

## 来源

- GitHub README:
  - https://github.com/z-lab/dflash/blob/main/README.md
- DFlash 实现:
  - https://github.com/z-lab/dflash/blob/main/dflash/model.py
- Hugging Face 模型集合:
  - https://huggingface.co/collections/z-lab/dflash
- 代表性配置：
  - https://huggingface.co/z-lab/Qwen3.5-27B-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/Qwen3.5-122B-A10B-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/gemma-4-31B-it-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/gemma-4-26B-A4B-it-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/gpt-oss-20b-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/gpt-oss-120b-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/Kimi-K2.5-DFlash/blob/main/config.json
  - https://huggingface.co/z-lab/LLaMA3.1-8B-Instruct-DFlash-UltraChat/blob/main/config.json

