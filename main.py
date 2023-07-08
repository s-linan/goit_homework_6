from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
from file_parser import get_extension

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True) # папка для архіву
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file, get_extension(filename).lower()) # TODO: Check!
    except shutil.ReadError:
        print("It's not archive")
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    for file in parser.IMAGES:
        handle_media(file, folder / 'Images')
    for file in parser.VIDEOS:
        handle_media(file, folder / 'Videos')
    for file in parser.DOCUMENTS:
        handle_media(file, folder / 'Documents')
    for file in parser.AUDIO:
        handle_media(file, folder / 'Audio')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'Archives')
    for file in parser.OTHER:
        handle_media(file, folder / 'Other')
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

if __name__ == '__main__':
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan}')
        main(folder_for_scan)
