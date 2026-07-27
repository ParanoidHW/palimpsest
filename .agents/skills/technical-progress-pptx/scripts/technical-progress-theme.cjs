"use strict";

const PptxGenJS = require("pptxgenjs");

const PALETTE = Object.freeze({
  canvas: "FBFAF7",
  navy: "102A43",
  slate: "334E68",
  muted: "829AB1",
  line: "D9E2EC",
  soft: "F1F3F5",
  amber: "F4C95D",
  salmon: "E98B73",
  white: "FBFAF7",
});

const FONT = process.env.PPTX_FONT || "MiSans";
const W = 17.7778;
const H = 10;

function newPresentation(meta = {}) {
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: "PROJECT_WIDE", width: W, height: H });
  pptx.layout = "PROJECT_WIDE";
  pptx.author = meta.author || "Codex";
  pptx.company = meta.company || "";
  pptx.subject = meta.subject || "Technical project progress";
  pptx.title = meta.title || "Technical Progress";
  pptx.lang = meta.lang || "zh-CN";
  pptx.theme = {
    headFontFace: FONT,
    bodyFontFace: FONT,
    lang: meta.lang || "zh-CN",
  };
  return pptx;
}

function addText(slide, text, opts = {}) {
  const base = {
    fontFace: FONT,
    fontSize: 15,
    color: PALETTE.slate,
    margin: 0,
    breakLine: false,
    fit: "shrink",
    valign: "top",
    ...opts,
  };
  slide.addText(text, base);
}

function addRect(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    fill: { color: opts.fill || PALETTE.canvas },
    line: { color: opts.line || PALETTE.line, width: opts.lineWidth ?? 1 },
    ...opts,
  });
}

function addLine(pptx, slide, x, y, w, h = 0, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x,
    y,
    w,
    h,
    line: {
      color: opts.color || PALETTE.line,
      width: opts.width ?? 1,
      dash: opts.dash || "solid",
      beginArrowType: opts.beginArrowType || "none",
      endArrowType: opts.endArrowType || "none",
    },
  });
}

function addFooter(slide, page, total, label = "内部工作文档 · 技术项目进展") {
  addText(slide, label, {
    x: 1.08,
    y: 9.55,
    w: 7.5,
    h: 0.18,
    fontSize: 9,
    color: PALETTE.muted,
  });
  addText(slide, `${String(page).padStart(2, "0")}/${String(total).padStart(2, "0")}`, {
    x: 15.95,
    y: 9.55,
    w: 0.75,
    h: 0.18,
    fontSize: 9,
    color: PALETTE.muted,
    align: "right",
  });
}

function addKicker(slide, text, x = 1.08, y = 0.56, color = PALETTE.muted) {
  addText(slide, text.toUpperCase(), {
    x,
    y,
    w: 8,
    h: 0.22,
    fontSize: 10,
    bold: true,
    color,
    charSpacing: 1.2,
  });
}

function addTitle(slide, text, opts = {}) {
  addText(slide, text, {
    x: opts.x ?? 1.08,
    y: opts.y ?? 1.05,
    w: opts.w ?? 14.6,
    h: opts.h ?? 0.72,
    fontSize: opts.fontSize ?? 32,
    bold: true,
    color: opts.color || PALETTE.navy,
    breakLine: false,
    fit: "shrink",
  });
}

function addSectionNumber(slide, text) {
  addText(slide, text, {
    x: 15.15,
    y: 0.48,
    w: 1.4,
    h: 0.85,
    fontSize: 72,
    bold: true,
    color: PALETTE.amber,
    transparency: 55,
    align: "right",
  });
}

function addDecision(slide, text, y = 8.55, color = PALETTE.navy) {
  addRect(
    { ShapeType: { rect: "rect" } },
    slide,
    { x: 1.08, y, w: 0.06, h: 0.52, fill: PALETTE.amber, line: PALETTE.amber, lineWidth: 0 }
  );
  addText(slide, text, {
    x: 1.34,
    y: y + 0.03,
    w: 14.7,
    h: 0.42,
    fontSize: 15,
    bold: true,
    color,
    valign: "middle",
  });
}

function addMetric(slide, value, label, opts = {}) {
  addText(slide, value, {
    x: opts.x,
    y: opts.y,
    w: opts.w,
    h: opts.valueH || 0.86,
    fontSize: opts.fontSize || 48,
    bold: true,
    color: opts.color || PALETTE.navy,
    align: opts.align || "left",
  });
  addText(slide, label, {
    x: opts.x,
    y: opts.y + (opts.labelOffset || 0.98),
    w: opts.w,
    h: opts.labelH || 0.48,
    fontSize: opts.labelSize || 14,
    color: opts.labelColor || PALETTE.slate,
    bold: opts.labelBold ?? false,
    align: opts.align || "left",
  });
}

function baseSlide(pptx, opts = {}) {
  const slide = pptx.addSlide();
  slide.background = { color: opts.background || PALETTE.canvas };
  return slide;
}

module.exports = {
  PptxGenJS,
  PALETTE,
  FONT,
  W,
  H,
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
};

