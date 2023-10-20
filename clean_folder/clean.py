import sys
import re
from pathlib import Path
import shutil

transliteration_dict = {
    ord('А'): 'A',
    ord('Б'): 'B',
    ord('В'): 'V',
    ord('Г'): 'G',
    ord('Д'): 'D',
    ord('Е'): 'E',
    ord('Ё'): 'YO',
    ord('Ж'): 'ZH',
    ord('З'): 'Z',
    ord('И'): 'I',
    ord('Й'): 'Y',
    ord('К'): 'K',
    ord('Л'): 'L',
    ord('М'): 'M',
    ord('Н'): 'N',
    ord('О'): 'O',
    ord('П'): 'P',
    ord('Р'): 'R',
    ord('С'): 'S',
    ord('Т'): 'T',
    ord('У'): 'U',
    ord('Ф'): 'F',
    ord('Х'): 'KH',
    ord('Ц'): 'TS',
    ord('Ч'): 'CH',
    ord('Ш'): 'SH',
    ord('Щ'): 'SCH',
    ord('Ъ'): '',
    ord('Ы'): 'Y',
    ord('Ь'): '',
    ord('Э'): 'E',
    ord('Ю'): 'YU',
    ord('Я'): 'YA',
    ord('а'): 'a',
    ord('б'): 'b',
    ord('в'): 'v',
    ord('г'): 'g',
    ord('д'): 'd',
    ord('е'): 'e',
    ord('ё'): 'yo',
    ord('ж'): 'zh',
    ord('з'): 'z',
    ord('и'): 'i',
    ord('й'): 'y',
    ord('к'): 'k',
    ord('л'): 'l',
    ord('м'): 'm',
    ord('н'): 'n',
    ord('о'): 'o',
    ord('п'): 'p',
    ord('р'): 'r',
    ord('с'): 's',
    ord('т'): 't',
    ord('у'): 'u',
    ord('ф'): 'f',
    ord('х'): 'kh',
    ord('ц'): 'ts',
    ord('ч'): 'ch',
    ord('ш'): 'sh',
    ord('щ'): 'sch',
    ord('ъ'): '',
    ord('ы'): 'y',
    ord('ь'): '',
    ord('э'): 'e',
    ord('ю'): 'yu',
    ord('я'): 'ya',
    ord('ї'): 'yi',
    ord('Ї'): 'YI',
    ord('є'): 'ye',
    ord('Є'): 'ye'
}

directory_from_console = Path(sys.argv[1])
# directory_from_console = Path(r'C:\Users\kivil\Desktop\Мотлох')
# Пути к папкам:
path_of_directory_images = Path(f'{directory_from_console}\\images')
path_of_directory_video = Path(f'{directory_from_console}\\video')
path_of_directory_documents = Path(f'{directory_from_console}\\documents')
path_of_directory_music = Path(f'{directory_from_console}\\music')
path_of_directory_archives = Path(f'{directory_from_console}\\archives')
path_of_directory_unknowns = Path(f'{directory_from_console}\\unknowns')

def main_function(path_of_directory_from_console):
    for item in path_of_directory_from_console.iterdir():
        sort_item(item)
    for item in path_of_directory_from_console.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                new_name_for_file_in_dir = normalize_name(str(file))
                file.rename(new_name_for_file_in_dir)
            new_name_for_directory = normalize_name(str(item))
            item.rename(new_name_for_directory)
        else:
            new_name_for_file = normalize_name(str(item))
            item.rename(new_name_for_file)

def sort_item(item_path):
    if item_path.is_dir() and item_path.name in ('archives', 'video', 'audio', 'documents', 'images'):
        return None
    if item_path.is_dir():
        if not any(item_path.iterdir()):
            item_path.rmdir()
        else:
            for item_2 in item_path.iterdir():
                sort_item(item_2)
    else:
        if item_path.suffix.upper() in ('.JPEG', '.PNG', '.JPG', '.SVG'):
            if not path_of_directory_images.exists():
                path_of_directory_images.mkdir()
            item_path.rename(path_of_directory_images / item_path.name)
        elif item_path.suffix.upper() in ('.AVI', '.MP4', '.MOV', '.MKV'):
            if not path_of_directory_video.exists():
                path_of_directory_video.mkdir()
            item_path.rename(path_of_directory_video / item_path.name)
        elif item_path.suffix.upper() in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'):
            if not path_of_directory_documents.exists():
                path_of_directory_documents.mkdir()
            item_path.rename(path_of_directory_documents / item_path.name)
        elif item_path.suffix.upper() in ('.MP3', '.OGG', '.WAV', '.AMR'):
            if not path_of_directory_music.exists():
                path_of_directory_music.mkdir()
            item_path.rename(path_of_directory_music / item_path.name)
        elif item_path.suffix.upper() in ('.ZIP', '.GZ', '.TAR'):
            if not path_of_directory_archives.exists():
                path_of_directory_archives.mkdir()
            item_path.rename(path_of_directory_archives / item_path.name)
            item_path_name_without_zip = re.sub(r'\..+', "", item_path.name)
            path_of_directory_for_new_archive = Path(path_of_directory_archives / item_path_name_without_zip)
            path_of_directory_for_new_archive.mkdir()
            shutil.unpack_archive(item_path, path_of_directory_for_new_archive)
        else:
            if not path_of_directory_unknowns.exists():
                path_of_directory_unknowns.mkdir()
            item_path.rename(path_of_directory_unknowns / item_path.name)
def normalize_name(item_path_str):
    item_name_match_file = re.search(r'[^\\]+\.\w+', item_path_str)
    item_name_match_dir = re.search(r'[^\\]+$', item_path_str)
    if item_name_match_file:
        item_name = item_name_match_file[0]
    else:
        item_name = item_name_match_dir[0]
    translated_item_name = item_name.translate(transliteration_dict)
    new_item_path_str = re.sub(item_name, translated_item_name, item_path_str)
    finall_new_item_path_str = re.sub(r'[^\w\d\\\.\:]', "_", new_item_path_str)
    return finall_new_item_path_str

main_function(directory_from_console)