# CANN Hardware Runtime

本目录记录昇腾 CANN 镜像、硬件信息入口，以及与昇腾运行环境相关的模型结构核查笔记。

## 阅读顺序

1. [镜像](镜像.md)：CANN 基础镜像选择和容器启动参数。
2. [硬件信息](硬件信息.md)：910B/C 资料入口。
3. [单边通信、Mooncake 与 Ascend ADXL/HIXL](topics/one-sided-communication-mooncake-ascend.md)：单边通信语义、Mooncake Transfer Engine，以及 Ascend HIXL/ADXL 的接入关系。
4. [DFlash 开源投机模型结构整理](DFlash 开源投机模型结构整理.md)：DFlash draft 模型公开配置和源码结构核查。

## 资产说明

- [assets/Pasted image 20260516160956.png](assets/Pasted image 20260516160956.png)：CANN 镜像选择说明截图，由 [镜像](镜像.md) 引用。

## 文档索引

### Topics

- [单边通信、Mooncake 与 Ascend ADXL/HIXL](topics/one-sided-communication-mooncake-ascend.md)
- [Mooncake Ascend 单边 Tensor 字典传输样例](topics/examples/mooncake_ascend_one_sided/README.md)

## 维护规则

- 运行命令和容器参数保留可复制格式。
- 硬件和镜像版本信息需要标注来源链接或更新时间。
- 与模型结构相关的结论优先写明公开配置、源码文件和匿名访问边界。
