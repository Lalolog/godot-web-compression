# Godot Web Compression

[Русская версия (README.md)](README.md)

A utility for compressing and decompressing Godot web builds using the gzip format. It helps reduce file sizes and speed up game loading in the browser.

---

## How It Works

1. **File Compression**

   - The `compress_and_update.py` script scans the specified directory for `.pck` and `.wasm` files.

   - Each file is compressed into `.gz` format.

2. **HTML & JS Updates**

   - The `index.html` file is automatically updated with `<script>` tags to include:

     - `decompress.js` — the decompression script

     - `fflate.js` — a JavaScript library for manual decompression

   - The `decompress.js` file is updated with the current list of files to intercept and decompress.

3. **Browser-Side Decompression**

   - `decompress.js` intercepts `fetch` requests for `.pck` and `.wasm` files.

   - It first attempts to load the corresponding `.gz` files.

   - If the browser supports [`DecompressionStream`](https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream), it is used.

   - Otherwise, the [`fflate`](https://github.com/101arrowz/fflate) library is used for manual decompression.

   - If the server has already decompressed the file (via `Content-Encoding: gzip`), no further decompression is performed.

### **Fallback Mechanism**

   - If loading or decompressing a `.gz` file fails (e.g. file missing or corrupted), the script falls back to fetching the original uncompressed file.

   - This ensures your game will still load, even if the compressed assets are unavailable or unsupported.

---

## Installation

```bash
git clone https://github.com/Lalolog/godot-web-compression
cd godot-web-compression
```

---

## Command Line Arguments

The `compress_and_update.py` script supports the following options:

| Argument               | Short Form | Description                                        | Default Value          |
|------------------------|------------|----------------------------------------------------|------------------------|
| `--source-dir`         | `-s`       | Path to directory containing `.pck` and `.wasm`    | `.`                    |
| `--decompress-js-path` | `-d`       | Path to `decompress.js`                            | `decompress.js`        |
| `--fflate-js-path`     | `-f`       | Path to `fflate.js`                                | `lib/fflate.js`        |
| `--index-html-path`    | `-i`       | Path to `index.html`                               | `index.html`           |

Example:

```bash
python compress_and_update.py \
  -s game \
  -d scripts/decompress.js \
  -f lib/fflate.js \
  -i index.html
```

The script will:
- Compress `.pck` and `.wasm` files into `.gz`
- Update the list in `decompress.js`
- Add `<script>` tags to `index.html`

---

## Example Project Structure

```
build/
├── compress_and_update.py
├── game/
│   ├── lib/
│   │   └── fflate.js
│   └── scripts/
│       └── decompress.js
│   ├── index.html
│   ├── index.pck
│   ├── index.pck.gz
│   ├── index.wasm
│   ├── index.wasm.gz
```

---

## Contact

[Telegram](https://t.me/Lalolog)
