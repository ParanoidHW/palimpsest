#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 input.pptx [output-dir] [--compat-libreoffice]" >&2
}

if [[ $# -lt 1 || $# -gt 3 ]]; then
  usage
  exit 2
fi

input_path="$(realpath "$1")"
output_dir="${2:-${input_path%.pptx}-qa}"
compat_mode="${3:-}"
if [[ -n "$compat_mode" && "$compat_mode" != "--compat-libreoffice" ]]; then
  usage
  exit 2
fi

mkdir -p "$output_dir"
output_dir="$(realpath "$output_dir")"

command -v unzip >/dev/null || {
  echo "missing dependency: unzip" >&2
  exit 1
}

unzip -t "$input_path" > "$output_dir/unzip-test.txt"
if python3 -m markitdown --help >/dev/null 2>&1; then
  python3 -m markitdown "$input_path" > "$output_dir/content.txt"
fi

rendered_by=""
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v powershell.exe >/dev/null && command -v wslpath >/dev/null; then
  input_win="$(wslpath -w "$input_path")"
  output_win="$(wslpath -w "$output_dir")"
  ps_script_win="$(wslpath -w "$script_dir/render-powerpoint.ps1")"
  if powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass \
    -File "$ps_script_win" \
    -InputPptx "$input_win" \
    -OutputDir "$output_win"; then
    rendered_by="powerpoint"
  else
    echo "warning: Microsoft PowerPoint rendering was unavailable or failed." >&2
  fi
else
  echo "warning: PowerPoint rendering is unavailable; visual QA is incomplete." >&2
fi

if [[ "$compat_mode" == "--compat-libreoffice" ]]; then
  for command_name in soffice pdftoppm; do
    command -v "$command_name" >/dev/null || {
      echo "missing compatibility dependency: $command_name" >&2
      exit 1
    }
  done
  profile_dir="$(mktemp -d /tmp/technical-progress-pptx-lo-XXXXXX)"
  work_dir="$(mktemp -d /tmp/technical-progress-pptx-render-XXXXXX)"
  trap 'rm -rf "$profile_dir" "$work_dir"' EXIT
  cp "$input_path" "$work_dir/input.pptx"
  soffice \
    "-env:UserInstallation=file://$profile_dir" \
    --headless \
    --convert-to pdf \
    --outdir "$work_dir" \
    "$work_dir/input.pptx"
  mkdir -p "$output_dir/libreoffice-compat"
  cp "$work_dir/input.pdf" "$output_dir/libreoffice-compat/rendered.pdf"
  pdftoppm -jpeg -r 150 \
    "$output_dir/libreoffice-compat/rendered.pdf" \
    "$output_dir/libreoffice-compat/slide"
fi

if command -v montage >/dev/null; then
  shopt -s nullglob nocaseglob
  powerpoint_images=("$output_dir"/powerpoint-slides/Slide*.png)
  if (( ${#powerpoint_images[@]} > 0 )); then
    montage "${powerpoint_images[@]}" \
      -thumbnail 520x \
      -tile 2x \
      -geometry +12+12 \
      -background '#E9ECEF' \
      "$output_dir/powerpoint-contact-sheet.jpg"
  fi
  compat_images=("$output_dir"/libreoffice-compat/slide-*.jpg)
  if (( ${#compat_images[@]} > 0 )); then
    montage "${compat_images[@]}" \
      -thumbnail 520x \
      -tile 2x \
      -geometry +12+12 \
      -background '#E9ECEF' \
      "$output_dir/libreoffice-compat/contact-sheet.jpg"
  fi
fi

if [[ "$rendered_by" != "powerpoint" ]]; then
  printf '%s\n' \
    "Visual QA incomplete: Microsoft PowerPoint rendering did not run." \
    "Do not use LibreOffice as the primary layout authority." \
    > "$output_dir/VISUAL_QA_INCOMPLETE.txt"
fi

echo "$output_dir"

