# PPT QA 记录

## 第一次生成

- 内容抽取：`python -m markitdown` 成功，11 张幻灯片均有标题、页码和预期文字。
- 发现问题：第 8 页使用纯 `=>` 连接，未清楚标明这是模型语义到 kernel 调用的 lowering；已改为 `semantic lowering`。

## 图文精读版复验

- 已重新生成图文精读版 PPTX：18 页，`markitdown` 可抽取所有页，无 `placeholder`、`xxxx` 或 `lorem`。
- PPTX 压缩包包含 12 个 `ppt/media` 图像和 12 个 slide image relationship；最终 Markdown 的 12 个图链接均指向存在的本地文件。
- 原论文图和本地 Cosmos 图共 34 个资产已经生成 contact sheet：`ppt_qa/paper_assets_contact_sheet.jpg`；机制图、性能图、caption 裁剪在该表上人工检查。
- 尝试三次 LibreOffice headless 转 PDF（默认环境、隔离 HOME/profile、图文精读版）均 exit 1，只输出 dconf 目录只读告警且没有 PDF。当前容器没有 `unoconv` 或其他 PPTX 渲染器，故 slide screenshot 级视觉 QA 被环境阻塞；PPTX 已通过内容、关系与资产静态检查。
