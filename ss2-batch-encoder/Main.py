from pathlib import Path
import argparse, sys
import Ss2BatchEncoder as ss2

def main(args: None) -> None:
    encoder = lambda path: ss2.encode_targa(args.dest, path)
    ss2.dir_apply_encoder(args.src, encoder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively encode exported IW3MVM targa sequences with Xvid."
    )
    parser.add_argument("src", type=Path, help="the directory to recursively traverse")
    parser.add_argument("dest", type=Path, help="the destination of the encoded videos")
    main(parser.parse_args())
