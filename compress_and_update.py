import argparse
import gzip
import os
import re
import shutil
from pathlib import Path


def resolve_path(base_dir: str, path: str) -> Path:
    """Resolve a path relative to base_dir if its not absolute"""
    path_obj = Path(path)
    if path_obj.is_absolute():
        return path_obj
    return Path(base_dir) / path


def compress_files(source_dir: str, files_to_compress: list[str]) -> None:
    """Compress all .pck and .wasm files to .gz"""
    for file in files_to_compress:
        input_path = Path(source_dir) / file
        output_path = input_path.with_suffix(input_path.suffix + ".gz")

        if output_path.exists():
            print(f"Skipping {input_path} as {output_path} already exists")
            continue

        try:
            with open(input_path, "rb") as file_input:
                with gzip.open(output_path, "wb") as file_output:
                    shutil.copyfileobj(file_input, file_output)
            print(f"Compressed {input_path} to {output_path}")
        except FileNotFoundError:
            print(f"Input file {input_path} not found")
        except PermissionError:
            print(f"No permission to write {output_path}")
        except Exception as error:
            print(f"Error compressing {input_path}: {error}")


def update_decompress_js(decompress_js_path: str, files_to_compress: list[str]) -> None:
    """Update the decompress.js file with the latest compressed files"""
    try:
        with open(decompress_js_path, "r") as file:
            content = file.read()

        new_files_list = ", ".join([f'"{file}"' for file in files_to_compress])

        if f"const files = [{new_files_list}];" in content:
            print(f"No changes needed in {decompress_js_path}")
            return

        updated_content = re.sub(
            r"const files = \[[^\]]*\];", f"const files = [{new_files_list}];", content
        )

        with open(decompress_js_path, "w", encoding="utf-8") as file:
            file.write(updated_content)
        print(f"Updated {decompress_js_path}: {new_files_list}")
    except FileNotFoundError:
        print(f"File {decompress_js_path} not found")
    except PermissionError:
        print(f"No permission to write {decompress_js_path}")
    except Exception as error:
        print(f"Error updating {decompress_js_path}: {error}")


def update_index_html(
    index_html_path: str, decompress_js_path: str, fflate_js_path: str
) -> None:
    """Add <script> tags for decompress.js and fflate to index.html"""
    try:
        with open(index_html_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = re.sub(
            r"<!-- Godot Web Compression Scripts -->.*?(?=</head>)",
            "",
            content,
            flags=re.DOTALL,
        )

        script_tags = (
            r"<!-- Godot Web Compression Scripts -->" + "\n"
            f'    <script src="{fflate_js_path}"></script>\n'
            f'    <script src="{decompress_js_path}"></script>\n'
        )
        updated_content = content.replace("</head>", f"{script_tags}</head>")

        with open(index_html_path, "w", encoding="utf-8") as file:
            file.write(updated_content)
        print(f"Updated {index_html_path} with {script_tags}")
    except FileNotFoundError:
        print(f"File {index_html_path} not found")
    except PermissionError:
        print(f"No permission to write {index_html_path}")
    except Exception as error:
        print(f"Error updating {index_html_path}: {error}")


def main(
    source_dir: str, decompress_js_path: str, fflate_js_path: str, index_html_path: str
):
    """Main function to process files"""

    source_dir_path = Path(source_dir)
    if not source_dir_path.is_dir():
        print(f"Directory {source_dir} not found")
        return

    decompress_js_full_path = resolve_path(source_dir, decompress_js_path)
    fflate_js_full_path = resolve_path(source_dir, fflate_js_path)
    index_html_full_path = resolve_path(source_dir, index_html_path)

    for path in [decompress_js_full_path, fflate_js_full_path, index_html_full_path]:
        if not path.exists():
            print(f"File {path} not found")
            return

    files_to_compress = [
        f for f in os.listdir(source_dir) if f.endswith(".pck") or f.endswith(".wasm")
    ]

    if not files_to_compress:
        print(f"No .pck or .wasm files found in {source_dir}")
        return

    compress_files(source_dir, files_to_compress)
    update_decompress_js(decompress_js_full_path, files_to_compress)
    update_index_html(index_html_full_path, decompress_js_path, fflate_js_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress and update Godot web build files"
    )
    parser.add_argument(
        "-s",
        "--source-dir",
        default=".",
        help="Directory with .pck and .wasm files",
    )
    parser.add_argument(
        "-d",
        "--decompress-js-path",
        default="decompress.js",
        help="Path to decompress.js",
    )
    parser.add_argument(
        "-f",
        "--fflate-js-path",
        default="lib/fflate.js",
        help="Path to fflate.js",
    )
    parser.add_argument(
        "-i",
        "--index-html-path",
        default="index.html",
        help="Path to index.html",
    )
    args = parser.parse_args()

    main(
        args.source_dir,
        args.decompress_js_path,
        args.fflate_js_path,
        args.index_html_path,
    )
