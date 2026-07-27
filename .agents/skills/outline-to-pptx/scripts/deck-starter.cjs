#!/usr/bin/env node
"use strict";

const path = require("path");
const {
  PALETTE,
  TYPE,
  newPresentation,
  baseSlide,
  addText,
  addRichText,
  criticalRun,
  addRect,
  addLine,
  addFooter,
  addRunningHeader,
  addTitle,
  addSectionNumber,
  addMetric,
} = require("./outline-pptx-theme.cjs");

const output = path.resolve(process.argv[2] || "outline-to-pptx-reference.pptx");
const pptx = newPresentation({
  title: "Outline to PPTX Reference",
  subject: "Light academic presentation generated from a Markdown outline",
});
const total = 3;

// Opening viewpoint
{
  const slide = baseSlide(pptx);
  addRunningHeader(slide, "开场 · 核心观点");
  addSectionNumber(slide, "01");
  addTitle(slide, "大纲的核心观点决定整份演示结构");
  addLine(pptx, slide, 1.08, 1.88, 15.55, 0);

  const stages = [
    ["读取", "识别标题、段落与视觉对象", "输入：Markdown 大纲"],
    ["组织", "合并相关信息并拆分独立观点", "中间产物：deck plan"],
    ["编排", "为每个观点选择合适页面范式", "输出：可编辑 PPTX"],
  ];
  stages.forEach(([title, note, artifact], index) => {
    const x = 1.08 + index * 5.15;
    if (index > 0) {
      addLine(pptx, slide, x - 0.62, 3.35, 0.44, 0, {
        color: PALETTE.muted,
        width: 1.5,
        endArrowType: "triangle",
      });
    }
    addText(slide, `0${index + 1}`, {
      x,
      y: 2.52,
      w: 0.6,
      h: 0.24,
      fontSize: TYPE.note,
      bold: true,
      color: PALETTE.critical,
    });
    addText(slide, title, {
      x,
      y: 3.02,
      w: 3.9,
      h: 0.38,
      fontSize: TYPE.body,
      bold: true,
      color: PALETTE.ink,
    });
    addText(slide, note, {
      x,
      y: 3.62,
      w: 4.05,
      h: 0.32,
      fontSize: TYPE.note,
      color: PALETTE.body,
    });
    addText(slide, artifact, {
      x,
      y: 4.08,
      w: 4.05,
      h: 0.28,
      fontSize: TYPE.note,
      color: PALETTE.muted,
    });
    addLine(pptx, slide, x, 4.58, 4.0, 0, { color: PALETTE.line });
  });

  addRichText(
    slide,
    [
      { text: "原则：" },
      criticalRun("先确定观点"),
      { text: "，再决定页面数量与视觉形式。" },
    ],
    {
      x: 1.08,
      y: 7.82,
      w: 13.6,
      h: 0.42,
      fontSize: TYPE.body,
      color: PALETTE.ink,
    }
  );
  addFooter(slide, 1, total);
}

// One slide, one viewpoint
{
  const slide = baseSlide(pptx);
  addRunningHeader(slide, "正文 · 信息组织");
  addSectionNumber(slide, "02");
  addTitle(slide, "每页只围绕一个观点组织信息");
  addLine(pptx, slide, 1.08, 1.88, 15.55, 0);

  addMetric(slide, "1 页", "对应一个观点", {
    x: 1.08,
    y: 2.62,
    w: 4.2,
  });
  addText(slide, "可选视觉对象", {
    x: 1.08,
    y: 4.25,
    w: 2.2,
    h: 0.32,
    fontSize: TYPE.body,
    bold: true,
    color: PALETTE.ink,
  });
  addText(slide, "图片 · 表格 · 图表 · 流程 · 时间线", {
    x: 1.08,
    y: 4.82,
    w: 4.7,
    h: 0.28,
    fontSize: TYPE.note,
    color: PALETTE.muted,
  });

  addLine(pptx, slide, 6.10, 2.40, 0, 4.72);
  addText(slide, "组织方式", {
    x: 6.72,
    y: 2.58,
    w: 2.4,
    h: 0.35,
    fontSize: TYPE.body,
    bold: true,
    color: PALETTE.ink,
  });
  addRichText(
    slide,
    [
      { text: "01  标题直接写观点，正文最多保留" },
      criticalRun("三组信息"),
      { text: "。" },
    ],
    {
      x: 6.72,
      y: 3.22,
      w: 8.8,
      h: 0.44,
      fontSize: TYPE.body,
    }
  );
  addRichText(
    slide,
    [
      { text: "02  视觉形式由信息关系决定，" },
      criticalRun("不为装饰而配图"),
      { text: "。" },
    ],
    {
      x: 6.72,
      y: 4.02,
      w: 8.8,
      h: 0.52,
      fontSize: TYPE.body,
    }
  );

  addRect(pptx, slide, {
    x: 6.72,
    y: 5.12,
    w: 8.72,
    h: 1.55,
    fill: PALETTE.soft,
    line: PALETTE.line,
  });
  addText(slide, "【待补充】视觉对象", {
    x: 7.02,
    y: 5.42,
    w: 3.2,
    h: 0.34,
    fontSize: TYPE.body,
    bold: true,
    color: PALETTE.critical,
  });
  addText(slide, "类型：____    标题 / caption：____    来源 / 备注：____", {
    x: 7.02,
    y: 6.05,
    w: 7.85,
    h: 0.28,
    fontSize: TYPE.note,
    color: PALETTE.body,
  });
  addText(slide, "大纲中的图片、表格、引用和占位符均应保留对应关系", {
    x: 1.08,
    y: 8.52,
    w: 12.2,
    h: 0.24,
    fontSize: TYPE.note,
    color: PALETTE.muted,
  });
  addFooter(slide, 2, total);
}

// Closing
{
  const slide = baseSlide(pptx);
  addRunningHeader(slide, "收束 · 结尾");
  addSectionNumber(slide, "03");
  addTitle(slide, "结尾回到观点并给出下一步");
  addLine(pptx, slide, 1.08, 1.88, 15.55, 0);

  const rows = [
    ["01", "结论", "复述整份演示希望受众记住的内容。"],
    ["02", "下一步", "保留大纲中已有的行动项与顺序。"],
    ["03", "待补字段", "继续显示缺失内容，不用推测替代。"],
  ];
  rows.forEach(([number, title, body], index) => {
    const y = 2.55 + index * 1.55;
    addText(slide, number, {
      x: 1.08,
      y,
      w: 0.6,
      h: 0.26,
      fontSize: TYPE.note,
      bold: true,
      color: PALETTE.critical,
    });
    addText(slide, title, {
      x: 2.05,
      y: y - 0.02,
      w: 3.6,
      h: 0.36,
      fontSize: TYPE.body,
      bold: true,
      color: PALETTE.ink,
    });
    addText(slide, body, {
      x: 6.02,
      y: y - 0.02,
      w: 8.8,
      h: 0.42,
      fontSize: TYPE.body,
      color: PALETTE.body,
    });
    addLine(pptx, slide, 2.05, y + 0.72, 13.0, 0);
  });

  addRichText(
    slide,
    [
      { text: "完成标准：页面结构与大纲一致，并在结尾" },
      criticalRun("回到观点"),
      { text: "。" },
    ],
    {
      x: 1.08,
      y: 8.10,
      w: 13.7,
      h: 0.44,
      fontSize: TYPE.body,
      color: PALETTE.ink,
    }
  );
  addFooter(slide, 3, total);
}

pptx.writeFile({ fileName: output });
console.log(output);
