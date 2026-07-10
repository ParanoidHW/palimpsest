# PPT QA 记录

## 第一次生成

- 内容抽取：`python -m markitdown` 成功，11 张幻灯片均有标题、页码和预期文字。
- 发现问题：第 8 页使用纯 `=>` 连接，未清楚标明这是模型语义到 kernel 调用的 lowering；已改为 `semantic lowering`。

## 修复后复验

- 已重新生成 PPTX，并以 `markitdown` 验证更新文本存在、没有 placeholder、11 页均可抽取。
- 尝试两次 LibreOffice headless 转 PDF（默认环境和隔离 HOME/profile）均 exit 1，只输出 dconf 目录只读告警且没有 PDF。当前容器没有 `unoconv` 或其他 PPTX 渲染器，故截图/视觉 QA 被环境阻塞；PPTX 本身通过 XML/内容抽取检查。
