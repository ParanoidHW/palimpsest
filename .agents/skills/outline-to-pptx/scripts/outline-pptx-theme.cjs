"use strict";

const path = require("path");
const PptxGenJS = require("pptxgenjs");
const STYLE = require(path.join(__dirname, "..", "references", "academic-light.style.json"));

const basePalette = STYLE.palette;
const PALETTE = Object.freeze({
  ...basePalette,
  // Compatibility aliases for existing task-local builders.
  navy: basePalette.ink,
  slate: basePalette.body,
  critical: basePalette.critical_red,
  salmon: basePalette.critical_red,
  amber: basePalette.critical_red,
});

const TYPE = Object.freeze({ ...STYLE.typography.sizes_pt });
const FONT_ZH = process.env.PPTX_FONT_ZH || STYLE.fonts.zh_primary;
const FONT_EN = process.env.PPTX_FONT_EN || STYLE.fonts.en_primary;
const FONT_FALLBACK = process.env.PPTX_FONT_FALLBACK || STYLE.fonts.fallback[0];
const FONT = FONT_ZH;
const W = STYLE.canvas.width_in;
const H = STYLE.canvas.height_in;

function fontForText(text) {
  const value = Array.isArray(text)
    ? text.map((run) => run.text || "").join("")
    : String(text ?? "");
  return /[\u3400-\u9fff]/u.test(value) ? FONT_ZH : FONT_EN;
}

function newPresentation(meta = {}) {
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: "PROJECT_WIDE", width: W, height: H });
  pptx.layout = "PROJECT_WIDE";
  pptx.author = meta.author || "Codex";
  pptx.company = meta.company || "";
  pptx.subject = meta.subject || "Presentation generated from a structured outline";
  pptx.title = meta.title || "Outline Presentation";
  pptx.lang = meta.lang || "zh-CN";
  pptx.theme = {
    headFontFace: FONT_ZH,
    bodyFontFace: FONT_ZH,
    lang: meta.lang || "zh-CN",
  };
  return pptx;
}

function addText(slide, text, opts = {}) {
  const base = {
    fontFace: opts.fontFace || fontForText(text),
    fontSize: TYPE.body,
    color: PALETTE.body,
    margin: 0,
    breakLine: false,
    valign: "top",
    ...opts,
  };
  slide.addText(text, base);
}

function addRichText(slide, runs, opts = {}) {
  const normalized = runs.map((run) => ({
    text: run.text,
    options: {
      fontFace: run.options?.fontFace || fontForText(run.text),
      fontSize: run.options?.fontSize || opts.fontSize || TYPE.body,
      color: run.options?.color || opts.color || PALETTE.body,
      ...run.options,
    },
  }));
  slide.addText(normalized, {
    margin: 0,
    breakLine: false,
    valign: "top",
    ...opts,
  });
}

function criticalRun(text, opts = {}) {
  return {
    text,
    options: {
      bold: true,
      color: PALETTE.critical,
      ...opts,
    },
  };
}

function addRect(pptx, slide, opts = {}) {
  const {
    fill = PALETTE.canvas,
    line = PALETTE.line,
    lineWidth = 1,
    ...shapeOpts
  } = opts;
  slide.addShape(pptx.ShapeType.rect, {
    ...shapeOpts,
    fill: { color: fill },
    line: { color: line, width: lineWidth },
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

function addFooter(slide, page, total, label = "演示文稿 · 可编辑版本") {
  addText(slide, label, {
    x: 1.08,
    y: 9.48,
    w: 7.5,
    h: 0.22,
    fontSize: TYPE.note,
    color: PALETTE.muted,
  });
  addText(slide, `${String(page).padStart(2, "0")}/${String(total).padStart(2, "0")}`, {
    x: 15.82,
    y: 9.48,
    w: 0.82,
    h: 0.22,
    fontSize: TYPE.note,
    color: PALETTE.muted,
    align: "right",
  });
}

function addRunningHeader(slide, text, x = 1.08, y = 0.48, color = PALETTE.muted) {
  addText(slide, text, {
    x,
    y,
    w: 12.8,
    h: 0.24,
    fontSize: TYPE.note,
    bold: true,
    color,
  });
}

function addKicker(slide, text, x = 1.08, y = 0.48, color = PALETTE.muted) {
  addRunningHeader(slide, text, x, y, color);
}

function addTitle(slide, text, opts = {}) {
  addText(slide, text, {
    x: opts.x ?? 1.08,
    y: opts.y ?? 1.02,
    w: opts.w ?? 14.9,
    h: opts.h ?? 0.62,
    fontSize: TYPE.title,
    bold: true,
    color: opts.color || PALETTE.ink,
    ...opts,
  });
}

function addSectionNumber(slide, text) {
  addText(slide, text, {
    x: 15.50,
    y: 0.42,
    w: 1.12,
    h: 0.32,
    fontSize: TYPE.note,
    bold: true,
    color: PALETTE.muted,
    align: "right",
  });
}

function addDecision(slide, text, y = 8.48, color = PALETTE.ink) {
  addRect(
    { ShapeType: { rect: "rect" } },
    slide,
    {
      x: 1.08,
      y,
      w: 0.06,
      h: 0.48,
      fill: PALETTE.critical,
      line: PALETTE.critical,
      lineWidth: 0,
    }
  );
  addText(slide, text, {
    x: 1.34,
    y: y + 0.01,
    w: 14.7,
    h: 0.44,
    fontSize: TYPE.body,
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
    h: opts.valueH || 0.62,
    fontSize: TYPE.title,
    bold: true,
    color: opts.color || PALETTE.critical,
    align: opts.align || "left",
  });
  addText(slide, label, {
    x: opts.x,
    y: opts.y + (opts.labelOffset || 0.72),
    w: opts.w,
    h: opts.labelH || 0.42,
    fontSize: TYPE.body,
    color: opts.labelColor || PALETTE.body,
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
  STYLE,
  PALETTE,
  TYPE,
  FONT,
  FONT_ZH,
  FONT_EN,
  FONT_FALLBACK,
  W,
  H,
  fontForText,
  newPresentation,
  baseSlide,
  addText,
  addRichText,
  criticalRun,
  addRect,
  addLine,
  addFooter,
  addRunningHeader,
  addKicker,
  addTitle,
  addSectionNumber,
  addDecision,
  addMetric,
};
