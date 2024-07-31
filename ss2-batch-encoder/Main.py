from pathlib import Path
import argparse, sys
import Ss2BatchEncoder as ss2

def main(args: None) -> None:
    encoder = lambda path: (
        ss2.encode_avi(args.dest, path) if args.avi else
        ss2.encode_targa(args.dest, path))
        
    ss2.dir_apply_encoder(args.src, encoder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively encode exported IW3MVM targa sequences with Xvid.")
    parser.add_argument("src", type=Path, help="the directory to recursively traverse")
    parser.add_argument("dest", type=Path, help="the destination of the encoded videos")
    parser.add_argument("--avi", action="store_true", help="encode IW3MVM avi source files")
    main(parser.parse_args())
