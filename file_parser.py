import sys
from pathlib import Path

IMAGES = []
VIDEOS = []
DOCUMENTS = []
AUDIO = []
ARCHIVES = []
OTHER = []

REGISTER_EXTENSION = {
    'JPEG': IMAGES, 'PNG': IMAGES, 'JPG': IMAGES, 'SVG': IMAGES, 'BMP': IMAGES,
    'AVI': VIDEOS, 'MP4': VIDEOS, 'MOV': VIDEOS, 'MKV': VIDEOS,
    'DOC': DOCUMENTS, 'DOCX': DOCUMENTS, 'TXT': DOCUMENTS, 'PDF': DOCUMENTS, 'XLSX': DOCUMENTS, 'PPTX': DOCUMENTS,
    'MP3': AUDIO, 'OGG': AUDIO, 'WAV': AUDIO, 'AMR': AUDIO,
    'ZIP': ARCHIVES, 'GZ': ARCHIVES, 'TAR': ARCHIVES
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper() # перетворюємо розширення файлу на назву папки .jpg -> JPG (суфікс[1:] пропускає 1 символ, тобто крапку)



def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступної папки
            # Перевіряємо, щоб папка не була тією, в яку ми складаємо файли
            if item.name not in ('images', 'videos', 'audio', 'documents', 'images', 'other'):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item) # рекурсія
            continue # переходимо до наступного елемента
        # Робота з файлом
        ext = get_extension(item.name) # беремо розширення файлу
        fullname = folder / item.name # беремо шлях до файлу
        if not ext: # якщо файл не має розширення то додаємо до невідомих
            OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # якщо не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                OTHER.append(fullname)

if __name__ == "__main__":
    folder_to_scan = sys.argv[1]
    print(f'Start in folder {folder_to_scan}')
    scan(Path(folder_to_scan))
    print(f'Images: {IMAGES}')
    print(f'Videos: {VIDEOS}')
    print(f'Documents: {DOCUMENTS}')
    print(f'Audio: {AUDIO}')
    print(f'Archives: {ARCHIVES}')
    print(f'Other: {OTHER}')
    print(f'Types of files in folder: {EXTENSION}')
    print(f'Unknown files of types: {UNKNOWN}')
    print(FOLDERS[::-1]) # виводить усі знайдені папки у нашій папці



