import subprocess, sys
from pathlib import Path, PurePath
from typing import List, Callable, Union

Encoding = str
Encoder = Callable[[Path], None]

def dir_apply_encoder(directory: Path, e: Encoder) -> None:
    """
    Recursively applies encoder `e` to all children of `directory`.
    """
    if not directory.exists() or not directory.is_dir():
        return

    for child in directory.iterdir():
        e(child)
        if child.is_dir():
            dir_apply_encoder(child, e)

def get_start_number(files: List[str]) -> int:
    """
    Returns the start number given a list of targa sequence file
    names.
    """
    return min(list(map(lambda f: int(f[-7:]), files)))

def encode_targa(dest: Path, src: Path) -> None:
    """
    Encodes a targa sequence if `src` matches a directory with a
    targa sequence. Exports result to `dest` using xvid
    encoding. Assumes directory **only** contains the set of targa
    images.
    """
    if not src.exists() or not src.is_dir():
        return

    paths = list(src.iterdir())
    if not all(path.is_file() and path.suffix == ".tga" for path in paths):
        return

    path_names = list(map(lambda p: p.stem, paths))
    encode(
        src / PurePath(path_names[0][:-7] + "%07d.tga"),
        dest / PurePath(f"{src.parent.stem}-{src.stem}").with_suffix(".avi"),
        get_start_number(path_names)
    )

def encode(src: Path, dest: Path, start_number: int) -> None:
    subprocess.run([
        "ffmpeg",
        "-start_number", str(start_number),
        "-i", str(src),
        "-vcodec", "mpeg4", "-vtag", "xvid",
        "-g", "32",
        "-qscale:v", "1",
        "-y",
        str(dest)
    ])
