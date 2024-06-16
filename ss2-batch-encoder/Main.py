from pathlib import Path
import argparse, sys
import Ss2BatchEncoder as ss2

def main(args: None) -> None:
    encoder = ss2.get_encoder(args.src_format)
    encoder_curried = lambda path: encoder(
        args.dest,
        args.encoding,
        path
    )
    ss2.dir_apply_encoder(args.src, encoder_curried)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively encode exported IW3MVM videos.")
    parser.add_argument("src", type=Path, help="the directory to recursively traverse")
    parser.add_argument("dest", type=Path, help="the destination of the encoded videos")
    parser.add_argument(
        "--format",
        type=str,
        choices=["targa", "avi", "both"],
        default="both",
        help="the file format(s) to encode",
        dest="src_format"
    )
    parser.add_argument(
        "--encoding",
        type=ss2.Encoding,
        choices=["xvid", "prores"],
        default="xvid",
        help="the encoding"
    )
    
    main(parser.parse_args())
