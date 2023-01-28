from os import listdir
from pathlib import Path
import shutil

IMAGES_SUFFIX = ('JPEG', 'PNG', 'JPG', 'SVG')
DOCUMENTS_SUFFIX = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PPT')
AUDIO_SUFFIX = ('MP3', 'OGG', 'WAV', 'AMR')
VIDEO_SUFFIX = ('AVI', 'MP4', 'MOV', 'MKV')
ARCHIVES_SUFFIX = ('ZIP', 'GZ', 'TAR')

def sort_archives(file_path: Path, out_dir: Path) -> str:
    """unpak archive to sub cat archives in directory like filename 

    Args:
        file_path (Path): archive filename
        out_dir (Path): destination directory

    Returns:
        str: directory name of ?err 
    """
    new_dir = str(out_dir.resolve()) + '/archives/' + file_path.stem
    try:
        Path(str(out_dir.resolve()) +
             '/archives').mkdir(exist_ok=True, parents=True)
        Path(new_dir).mkdir(exist_ok=True, parents=True)
    except OSError:
        new_dir = "?errOS"

    try:
        shutil.unpack_archive(file_path.resolve(), new_dir)
    except shutil.ReadError:
        new_dir = "?errAR"

    try:
        file_path.resolve().unlink()
    except FileNotFoundError:
        new_dir = "?errDF"

    return new_dir


def move_file(file_path: Path, out_dir: Path, destany: str) -> str:
    """move file to sub directory in sub directory destany 

    Args:
        file_path (Path): archive filename
        out_dir (Path): destination directory

    Returns:
        str: normalized new file name of ?err 
    """
    new_f = str(out_dir.resolve()) + '/' + destany + '/' + file_path.stem + file_path.suffix
    try:
        Path(str(out_dir.resolve()) + '/' +
             destany).mkdir(exist_ok=True, parents=True)
        shutil.move(str(file_path.resolve()), new_f)
    except OSError:
        new_f = "?errOS"
    finally:
        return new_f


def sort_dir(path: Path, out_dir: Path) -> dict:
    """sorting dir and file to sub directory 

    Args:
        path (Path): soure directory
        out_dir (Path): destination directory

    Returns:
        dict: 
            result_list = {'images': [], 'documents': [],
                   'audio': [], 'video': [], 'archives': []}
            to_do_suffix = set()
            unknown_suffix = set()
            trobles_list = []
    """

    result_list = {'images': [], 'documents': [],
                   'audio': [], 'video': [], 'archives': []}
    to_do_suffix = set()
    unknown_suffix = set()
    trobles_list = []

    for p in path.iterdir():
        if p.is_dir():
            if not str(p.name) in result_list.keys():
                # магія
                dir_res = sort_dir(p, out_dir)
                # доповнення результатів теки
                for key in result_list.keys():
                    result_list[key].extend(dir_res['result_list'][key])
                to_do_suffix = to_do_suffix | dir_res['to_do_suffix']
                unknown_suffix = unknown_suffix | dir_res['unknown_suffix']
                trobles_list.extend(dir_res['trobles_list'])

                # перевірка на пусту теку
                if not listdir(p):
                    # видалення теки
                    try:
                        p.rmdir()
                    except OSError:
                        trobles_list.append(
                            f'empty dir {p.resolve} dont want to die')

        else:
            if p.suffix.removeprefix('.').upper() in IMAGES_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'images')
                if res[0] != '?':
                    result_list['images'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in DOCUMENTS_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'documents')
                if res[0] != '?':
                    result_list['documents'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in AUDIO_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'audio')
                if res[0] != '?':
                    result_list['audio'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in VIDEO_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'video')
                if res[0] != '?':
                    result_list['video'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in ARCHIVES_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = sort_archives(p, out_dir)
                if res[0] != '?':
                    result_list['archives'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            else:
                unknown_suffix.add(p.suffix)

    return {'result_list': result_list, 'to_do_suffix': to_do_suffix, 'unknown_suffix': unknown_suffix, 'trobles_list': trobles_list}
