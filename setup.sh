#!/bin/sh
# One-time (and safe to re-run) setup for this Mac. Run from the project root: ./setup.sh
set -e
cd "$(dirname "$0")"
command -v brew >/dev/null || { echo "Install Homebrew first: https://brew.sh"; exit 1; }
for p in ffmpeg espeak-ng; do brew list $p >/dev/null 2>&1 || brew install $p; done
brew list --cask font-inter >/dev/null 2>&1 || brew install --cask font-inter
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip numpy onnxruntime playwright
.venv/bin/python -m playwright install chromium
mkdir -p tts && cd tts
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f kokoro-v1.0.onnx ] || curl -sSLO $R/kokoro-v1.0.onnx
[ -f voices-v1.0.bin ] || curl -sSLO $R/voices-v1.0.bin
[ -f config.json ] || curl -sSL -o config.json https://raw.githubusercontent.com/thewh1teagle/kokoro-onnx/main/src/kokoro_onnx/config.json
cd ..
[ -d geo/wgj ] || { git clone -q --depth 1 https://github.com/johan/world.geo.json geo/wgj && rm -rf geo/wgj/.git; }
echo "Setup OK"
