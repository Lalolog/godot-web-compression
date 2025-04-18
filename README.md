# Godot Web Compression

[English version (README_EN.md)](README_EN.md)

Утилита для сжатия и распаковки веб-билдов Godot с использованием формата gzip. Позволяет уменьшить размер файлов и ускорить загрузку игры в браузере.

---

## Как это работает

1. **Сжатие файлов**

   - Скрипт `compress_and_update.py` находит все файлы с расширениями `.pck` и `.wasm` в указанной директории.

   - Каждый файл сжимается в формат `.gz`.

2. **Обновление HTML и JS**

   - В файл `index.html` автоматически добавляются теги `<script>` для подключения:

     - `decompress.js` — скрипт распаковки

     - `fflate.js` — JS-библиотека для распаковки в браузере

   - Файл `decompress.js` обновляется с актуальным списком файлов для перехвата и распаковки.

3. **Распаковка в браузере**

   - `decompress.js` перехватывает вызовы `fetch` к `.pck` и `.wasm` файлам.

   - Сначала производится попытка загрузить соответствующие `.gz` версии.

   - Если браузер поддерживает [`DecompressionStream`](https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream), используется он.

   - В противном случае применяется библиотека [`fflate`](https://github.com/101arrowz/fflate) для распаковки вручную.

   - Если сервер уже распаковал файл (`Content-Encoding: gzip`), повторная распаковка не выполняется.

### **Fallback-механизм**

   - Если загрузка `.gz` файла или его распаковка завершилась с ошибкой (например, файл отсутствует или повреждён), скрипт пытается загрузить оригинальный несжатый файл.

   - Это гарантирует, что игра всё равно загрузится, даже если сжатые ресурсы недоступны или не поддерживаются браузером.


---

## Установка

```bash
git clone https://github.com/Lalolog/godot-web-compression
cd godot-web-compression
```

---

## Аргументы командной строки

Скрипт `compress_and_update.py` поддерживает следующие параметры:

| Аргумент               | Сокращение | Описание                                     | Значение по умолчанию |
|------------------------|------------|----------------------------------------------|------------------------|
| `--source-dir`         | `-s`       | Путь к папке с файлами `.pck` и `.wasm`      | `.`                    |
| `--decompress-js-path` | `-d`       | Путь к файлу `decompress.js`                 | `decompress.js`        |
| `--fflate-js-path`     | `-f`       | Путь к файлу `fflate.js`                     | `lib/fflate.js`        |
| `--index-html-path`    | `-i`       | Путь к файлу `index.html`                    | `index.html`           |

Пример запуска:

```bash
python compress_and_update.py \
  -s game \
  -d scripts/decompress.js \
  -f lib/fflate.js \
  -i index.html

```

Скрипт:
- Сожмeт `.pck` и `.wasm` файлы в `.gz`
- Обновит список в `decompress.js`
- Добавит теги `<script>` в `index.html`

---

## Пример структуры проекта

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

## Связь
[Telegram](https://t.me/Lalolog)
