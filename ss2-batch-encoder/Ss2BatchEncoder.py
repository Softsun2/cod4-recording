import subprocess, sys
from pathlib import Path, PureWindowsPath
from typing import List, Callable, Union

Encoding = str
Encoder = Callable[[Path], None]
Xvid = "xvid"
Prores = "prores"
Encodings = [Xvid, Prores]

def get_encoder(src_format: str) -> Callable[[Path, Encoding, Path], None]:
    if src_format == "targa":
        return encode_targa
    elif src_format == "avi":
        return encoder_avi
    elif src_format == "both":
        return encode_both
    else:
        sys.exit(1)

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
    return min(list(map(lambda f: int(f[-7:]), files)))

def encode_targa(dest: Path, encoding: Encoding, src: Path) -> None:
    """
    Encodes a targa sequence if `src` matches a directory with a
    targa sequence. Exports result to `dest` using `encoding`. Returns
    whether the operation succeeded. Assumes directory **only**
    contains the set of targa images.
    """
    if not src.exists() or not src.is_dir():
        return

    paths = list(src.iterdir())
    if not all(path.is_file() and path.suffix == ".tga" for path in paths):
        return

    path_names = list(map(lambda p: p.stem, paths))
    encode(
        src / PureWindowsPath(path_names[0][:-7] + "%07d.tga"),
        dest / PureWindowsPath(f"{src.parent.stem}-{src.stem}.avi"),
        encoding,
        get_start_number(path_names)
    )

def encode_avi(dest: Path, encoding: Encoding, src: Path) -> None:
    """
    Encodes an avi video if `src` matches an avi video. Exports to
    `dest` using `encoding`. Returns whether the operation succeeded.
    """
    if not src.exists() or not src.is_file() or src.suffix != ".avi":
        return
    
    encode(src, dest, encoding)

def encode_both(dest: Path, encoding: Encoding, src: Path) -> None:
    return

def encode(
    src: Path,
    dest: Path,
    encoding: Encoding,
    start_number: Union[int, None] = None
) -> None:
    if encoding == Xvid:
        command = [
            "ffmpeg",
            "-start_number", str(start_number),
            "-i", str(src),
            "-vcodec", "mpeg4", "-vtag", "xvid",
            "-g", "32",
            "-qscale:v", "1",
            "-y",
            str(dest)
        ]
        subprocess.run(command)
    elif encoding == Prores:
        pass
    else:
        # exit
        pass
    return
