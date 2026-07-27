#!/usr/bin/env node
"use strict";

const path = require("path");
const {
  PALETTE,
  newPresentation,
  baseSlide,
  addText,
  addRect,
  addLine,
  addFooter,
  addKicker,
  addTitle,
  addSectionNumber,
  addDecision,
  addMetric,
} = require("./technical-progress-theme.cjs");

const output = path.resolve(process.argv[2] || "technical-progress-example.pptx");
const pptx = newPresentation({
  title: "Technical Progress Example",
  subject: "Project-level technical presentation style",
});
const total = 3;

// Cover
{
  const slide = baseSlide(pptx);
  addLine(pptx, slide, 1.08, 0.58, 0.55, 0, { color: PALETTE.amber, width: 3 });
  addKicker(slide, "TECHNICAL PROGRESS — PROJECT UPDATE", 1.08, 0.78);
  addTitle(slide, "项目技术进展", { y: 1.72, w: 8.7, fontSize: 44 });
  addText(slide, "把阶段性指标，转化为可验证的工程结论。", {
    x: 1.08,
    y: 2.72,
    w: 8.6,
    h: 0.42,
    fontSize: 20,
    color: PALETTE.navy,
  });
  addText(slide, "用一行说明项目背景、当前覆盖范围和本次汇报要回答的问题。", {
    x: 1.08,
    y: 3.48,
    w: 8.2,
    h: 0.65,
    fontSize: 15,
    color: PALETTE.slate,
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 11.35,
    y: 1.72,
    w: 3.75,
    h: 3.75,
    fill: { color: PALETTE.soft },
    line: { color: PALETTE.soft, width: 0 },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 12.95,
    y: 2.08,
    w: 1.15,
    h: 1.15,
    fill: { color: PALETTE.amber },
    line: { color: PALETTE.amber, width: 0 },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 11.95,
    y: 3.55,
    w: 1.65,
    h: 1.65,
    fill: { color: PALETTE.navy },
    line: { color: PALETTE.navy, width: 0 },
  });
  addFooter(slide, 1, total);
}

// Result
{
  const slide = baseSlide(pptx);
  addKicker(slide, "RESULTS");
  addTitle(slide, "主指标达到目标，但结论仍受环境边界约束");
  addSectionNumber(slide, "01");
  addLine(pptx, slide, 1.08, 2.05, 15.55, 0, { color: PALETTE.line, width: 1 });
  addMetric(slide, "2.2×", "相对基线吞吐提升", {
    x: 1.08,
    y: 2.72,
    w: 4.2,
    fontSize: 72,
  });
  addText(slide, "测量环境", {
    x: 1.08,
    y: 4.55,
    w: 2.0,
    h: 0.24,
    fontSize: 12,
    bold: true,
    color: PALETTE.muted,
  });
  addText(slide, "数据集 · 并发 · 硬件 · 功能开关", {
    x: 1.08,
    y: 4.98,
    w: 4.5,
    h: 0.34,
    fontSize: 15,
    color: PALETTE.slate,
  });
  addLine(pptx, slide, 6.15, 2.45, 0, 3.75, { color: PALETTE.line, width: 1 });
  addMetric(slide, "88%", "首 token 接受率", {
    x: 6.85,
    y: 2.75,
    w: 3.0,
    fontSize: 44,
  });
  addMetric(slide, "75%", "平均接受率", {
    x: 10.25,
    y: 2.75,
    w: 3.0,
    fontSize: 44,
  });
  addText(slide, "边界：该结果来自轻量化框架，不代表真实 Serving 的端到端收益。", {
    x: 6.85,
    y: 4.82,
    w: 8.9,
    h: 0.58,
    fontSize: 15,
    bold: true,
    color: PALETTE.salmon,
  });
  addDecision(slide, "判断：结果显示性能潜力；下一步进入真实框架完成证据闭环。");
  addFooter(slide, 2, total);
}

// Closing
{
  const slide = baseSlide(pptx, { background: PALETTE.navy });
  addKicker(slide, "NEXT STEPS", 1.08, 0.70, PALETTE.amber);
  addTitle(slide, "下一步：完成三个验证闭环", {
    y: 1.20,
    w: 13.8,
    fontSize: 40,
    color: PALETTE.white,
  });
  addLine(pptx, slide, 1.08, 2.25, 15.55, 0, { color: "3E4C5E", width: 1 });
  const columns = [
    ["01", "真实框架验证", "补齐端到端吞吐、TPOT、P99 与稳定性。"],
    ["02", "补齐证据链", "回填 PR、配置、测量口径与缺失数据。"],
    ["03", "提升训练质量", "建立可复现归因矩阵并关闭质量差距。"],
  ];
  columns.forEach(([num, title, body], i) => {
    const x = 1.08 + i * 5.25;
    addText(slide, num, {
      x,
      y: 2.80,
      w: 0.62,
      h: 0.25,
      fontSize: 12,
      bold: true,
      color: PALETTE.amber,
    });
    addText(slide, title, {
      x: x + 0.82,
      y: 2.76,
      w: 3.7,
      h: 0.35,
      fontSize: 18,
      bold: true,
      color: PALETTE.white,
    });
    addText(slide, body, {
      x: x + 0.82,
      y: 3.38,
      w: 3.75,
      h: 0.78,
      fontSize: 14,
      color: "B8C4D0",
    });
  });
  addLine(pptx, slide, 1.08, 7.25, 15.55, 0, { color: "3E4C5E", width: 1 });
  addText(slide, "接受率是中间指标，真实吞吐才是结论。", {
    x: 1.08,
    y: 8.12,
    w: 10.0,
    h: 0.38,
    fontSize: 18,
    bold: true,
    color: PALETTE.amber,
  });
  addFooter(slide, 3, total, "内部工作文档 · 技术项目进展");
}

pptx.writeFile({ fileName: output });
console.log(output);

