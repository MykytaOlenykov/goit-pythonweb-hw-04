import asyncio
import logging
import argparse
from pathlib import Path

from aiofile import AIOFile


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(file: Path, dst_folder: Path):
    ext = file.suffix.lstrip(".") or "other"
    target_folder = dst_folder / ext

    try:
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file.name

        async with AIOFile(file, "rb") as src, AIOFile(target_file, "wb") as dst:
            content = await src.read()
            await dst.write(content)

        logging.info(f"Файл {file} успішно скопійовано в {target_file}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання {file}: {e}")


async def read_folder(src_folder: Path, dst_folder: Path):
    if not src_folder.exists():
        logging.error(f"Папка {src_folder} не існує")
        return

    if not src_folder.is_dir():
        logging.error(f"{src_folder} не є папкою")
        return

    tasks = [
        copy_file(item, dst_folder) for item in src_folder.rglob("*") if item.is_file()
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронне копіювання файлів")
    parser.add_argument("src_folder", type=str, help="Вихідна папка")
    parser.add_argument("dst_folder", type=str, help="Цільова папка")
    args = parser.parse_args()

    src_path = Path(args.src_folder)
    dst_path = Path(args.dst_folder)

    asyncio.run(read_folder(src_path, dst_path))
