# AscendCraft

## 资料边界

- 用途：记录 AscendCraft 的 DSL-guided transcompilation 路线和 AscendC kernel generation 观点。
- 本地资产：[assets/Pasted image 20260614223507.png](assets/Pasted%20image%2020260614223507.png)。
- 相关索引：[Kernel Agents Paper Index](0.%20Awesome%20Papers%20on%20LLM&Agent%20for%20kernel.md)。

![AscendCraft overview](assets/Pasted%20image%2020260614223507.png)

## 整体总结

这篇论文提出了 **AscendCraft**，这是一个利用大语言模型（LLM）通过领域特定语言（DSL）引导，自动生成华为昇腾（Ascend）NPU 高性能算子内核（Kernel）的框架。

以下是该研究提出的问题、解决思路和方案的详细解释：

---

## 1. 核心问题 (The Problem)

在深度学习领域，算子的执行效率至关重要，但为特定的加速器（如 NPU）开发高性能算子面临以下挑战：

*   **编程模型极其复杂：** 昇腾的 AscendC 编程模型涉及复杂的内存分级（Global Memory, L1, UB, L0 等）、严格的内存对齐要求（32字节）以及精细的流水线并行控制（CopyIn-Compute-CopyOut）。
*   **LLM 知识匮乏：** 与 CUDA 或 Triton 不同，AscendC 的公开代码库、文档和社区讨论非常稀少。这导致现有的 LLM 直接生成 AscendC 代码的正确率极低（根据文中提到的 MultiKernelBench 测试，正确率不足 5%）。
*   **容错率低：** 低级硬件编程中微小的语法或逻辑错误（如非对齐访问）就会导致编译失败或运行奔溃。

---

## 2. 解决思路 (The Strategy)

论文的核心思路是：**不在底层细节上硬碰硬，而是通过引入一个“抽象桥梁”（DSL）来降低生成难度。**

*   **引入轻量化 DSL：** 设计一种易于 LLM 理解的领域特定语言。这种语言隐藏了非本质的复杂性（如繁琐的对齐参数配置），但保留了关键的硬件语义（如分块策略和流水线结构）。
*   **两阶段分层生成：** 
    1.  **高层逻辑设计：** 让 LLM 先用 DSL 表达算子的核心算法、分块（Tiling）方案和数据流。
    2.  **结构化翻译（下放）：** 通过一系列受约束的“翻译步骤”（Transcompilation Passes），将 DSL 逐步降低（Lowering）到最终的 AscendC 代码。

---

## 3. 具体方案 (The Solution: AscendCraft)

### A. DSL 设计原则
AscendCraft 提出的 DSL 具有以下特点：
*   **主机-核函数分离：** 主机端（Host）负责全局规划（分块、核心分配）；内核端（Kernel）负责片上计算。
*   **显式分阶段执行：** 强制代码结构划分为 `copyin`、`compute` 和 `copyout` 三个块，对应昇腾 AICore 的流水线模型。
*   **自动处理复杂性：** 诸如 `DataCopyPad` 等涉及复杂对齐参数的底层指令，在 DSL 中被抽象成简单的计算原语。

### B. 自动化流水线
AscendCraft 的工作流程分为两个主要阶段：

1.  **DSL 代码生成：**
    *   使用类别特定的“专家示例”（Expert Examples）作为提示（Prompt），引导 LLM 生成 DSL。
    *   LLM 只需要关注分块因子和核心逻辑，而不必担心 C++ 语法细节。

2.  **四步结构化翻译（Transcompilation）：**
    *   **Pass 1 (Host)：** 翻译主机端代码，计算 Tiling 参数。
    *   **Pass 2 (Init)：** 初始化内核状态、管理片上内存队列（TQue/TBuf）。
    *   **Pass 3 (Compute)：** 将 DSL 的逻辑块翻译成特定的 AICore 函数，并插入队列同步指令。
    *   **Pass 4 (Refinement)：** 针对硬件边缘情况（如非均匀形状）自动调整内存对齐和填充（Padding）。

### C. 编译反馈循环
在翻译过程中，框架会自动调用昇腾编译器（CCE）。如果编译失败，会将错误信息反馈给 LLM 进行自我修正（Self-correction），显著提高了稳健性。

---

## 4. 实验结果 (Key Findings)

*   **极高的正确性：** 在 MultiKernelBench 的 52 个算子测试中，实现了 **98.1% 的编译成功率** 和 **90.4% 的功能正确率**。
*   **性能竞争力：** 约 **46.2%** 的生成算子性能达到或超过了 PyTorch Eager 模式。
*   **泛化能力：** 在 DeepSeek 提出的最新 **mHC 架构** 算子上，AscendCraft 仅需一次尝试就生成了正确算子，并比 PyTorch Eager 模式快了 3 到 6 倍，经过专家微调后加速比可达 15.9 倍。

---

## 总结

**AscendCraft** 的意义在于证明了：**对于缺乏语料库的专用硬件，与其通过海量数据训练 LLM，不如通过设计合理的抽象层（DSL）和分步骤的结构化翻译，让现有的通用 LLM 也能编写出正确的底层高性能代码。**

> "AscendCraft introduces a lightweight DSL that abstracts non-essential complexity while explicitly modeling Ascend-specific execution semantics." [Abstract](https://alphaxiv.org/abs/2601.22760v1?page=1)


# DSL和转移ASC来源
关于 DSL 的来源以及转译过程的实现，这篇论文的一个核心特点是：**它并不依赖于大规模的深度学习训练，而是基于“提示工程（Prompt Engineering）”和“结构化规则”驱动的 LLM 转换。**

以下是针对你问题的详细解答：

## 1. DSL 是怎么来的？（设计来源）

论文中的 DSL 并不是通过机器学习“学”出来的，而是由具有 **昇腾硬件背景的专家手动设计** 出来的。它的设计目标是作为 LLM 和底层 C++ 代码之间的“减震器”。# 整体总结

*   **借鉴成熟模型：** DSL 的语法风格借鉴了 **Triton**（一种流行的 GPU 算子开发语言）。这种风格对 LLM 非常友好，因为它结构紧凑、逻辑清晰，强调分块（Tiling）和数据流。
*   **硬件语义对齐：** 专家将昇腾 AICore 的核心特性（如 `Unified Buffer` 内存布局、`CopyIn-Compute-CopyOut` 三阶段流水线）提取出来，变成了 DSL 的强制性语法结构。
*   **抽象复杂细节：** 专家识别出 AscendC 中最让 LLM 头疼的部分（比如复杂的内存对齐参数计算），并在 DSL 中将其简化。
    > "The DSL adopts a compact and regular programming structure that reduces syntactic verbosity and enforces clear control flow." [DSL Design](https://alphaxiv.org/abs/2601.22760v1?page=2)

---

## 2. “转译”是怎么实现的？（是否需要训练？）

这是一个非常关键的点：**AscendCraft 的转译过程不需要对 LLM 进行专门的微调（Fine-tuning）训练。** 它使用的是现成的商业大模型（如 DeepSeek-V2 或 Claude），通过以下机制完成转换：

### A. 基于规则的提示词（In-Context Learning）
研究者为每一个转译步骤（Pass）编写了极其详细的 **Prompt 指南**。这些指南包含：
*   **映射映射表：** 告诉 LLM，DSL 里的某个关键字（如 `ub_buffer`）必须对应 AscendC 里的哪个数据结构（如 `TQue` 或 `TBuf`）。
*   **API 知识库：** 把 AscendC 相关的 API 文档片段直接喂给 LLM，让它知道如何调用底层的 `DataCopy` 或计算指令。
*   **少样本示例（Few-shot）：** 提供几组“DSL 到 AscendC”的翻译范例，让 LLM 模仿其翻译逻辑。

### B. 分阶段（Multi-Pass）的流水线化处理
为了降低 LLM 的幻觉和出错率，转译被拆解成了四个串行的任务，而不是一次性生成：
1.  **Host 转译：** 只让 LLM 翻译主机端计算分块逻辑的代码。
2.  **Kernel 初始化转译：** 只处理内核端的内存申请和变量初始化。
3.  **计算逻辑转译：** 将 DSL 的计算指令一对一映射到 AscendC API。
4.  **对齐修正：** 最后由 LLM 检查是否满足硬件的 32 字节对齐要求，并添加 `DataCopyPad`。

### C. 闭环修正（无需重新训练的“学习”）
如果在转译过程中生成的代码报错，框架会捕获编译器的错误信息（Error Log），将其作为反馈再次发送给 LLM。这种 **“编译-报错-修正”** 的循环在逻辑上替代了传统的模型训练，使模型能够根据具体的任务场景动态调整输出。
> "If compilation errors occur, the error messages are fed back to the LLM, which is prompted to revise and fix the code before proceeding to the next pass." [Feedback](https://alphaxiv.org/abs/2601.22760v1?page=7)

---

## 总结

*   **DSL 的来源：** 领域专家根据昇腾硬件特性手动设计的逻辑抽象层。
*   **转译的训练：** **没有进行参数级的模型训练。** 它是通过 **结构化的 Prompt 工程**、**领域专家提供的 Few-shot 示例** 以及 **多步下放（Lowering）策略**，利用 LLM 现有的推理和代码生成能力来完成的。

这种方法的优势在于：即使没有几万行 AscendC 代码去喂给模型做训练，只要有几个高质量的专家模板，就能让通用大模型胜任 NPU 内核开发的重任。
