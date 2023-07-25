from pathlib import Path
import shutil
import sys
import re

IMAGES = []
DOCUMENTS = []
AUDIO = []
VIDEO = []
ARCHIVES = []
OTHER = []

FOLDERS = []

REGISTER_EXTENSION = {
    "JPEG": IMAGES,
    "JPG": IMAGES,
    "BMP": IMAGES,
    "PNG": IMAGES,
    "SVG": IMAGES,
    "TXT": DOCUMENTS,
    "DOCX": DOCUMENTS,
    "MP3": AUDIO,
    "AVI": VIDEO,
    "ZIP": ARCHIVES,
}


CYRILLIC_SYMBOLS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "g",
    "d",
    "e",
    "ie",
    "zh",
    "z",
    "y",
    "i",
    "i",
    "i",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "kh",
    "ts",
    "ch",
    "sh",
    "shch",
    "",
    "yu",
    "ia",
)

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    right_name = name.translate(TRANS)
    right_name = re.sub(r"\W", "_", right_name)
    return right_name


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    EXTENSION = set()
    UNKNOWN = set()
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in (
                "archives",
                "video",
                "audio",
                "documents",
                "images",
            ):
                FOLDERS.append(item)
                scan(item)
            continue

        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                OTHER.append(fullname)
    return EXTENSION, UNKNOWN


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.stem) + filename.suffix))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.stem) + filename.suffix))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.stem)
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:
        print("It is not archive")
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


def main(folder: Path):
    scan(folder)
    for file in IMAGES:
        handle_media(file, folder / "images")
    for file in DOCUMENTS:
        handle_media(file, folder / "documents")
    for file in AUDIO:
        handle_media(file, folder / "audio")
    for file in VIDEO:
        handle_media(file, folder / "video")

    for file in OTHER:
        handle_media(file, folder / "other")
    for file in ARCHIVES:
        handle_archive(file, folder / "archives")

    for folder in FOLDERS[::-1]:
        handle_folder(folder)


def clean_folder():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        main(folder_for_scan.resolve())
        print(f"Images: {IMAGES}")
        print(f"Documents: {DOCUMENTS}")
        print(f"Audio: {AUDIO}")
        print(f"Video: {VIDEO}")
        print(f"Archives: {ARCHIVES}")
        print(f"MY_OTHER: {OTHER}")
