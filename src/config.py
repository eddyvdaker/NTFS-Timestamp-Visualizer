import argparse
import os


class Config(object):
    input_path: str
    output_path: str
    output_file: str
    filter: str
    dpi: int
    out_format: str
    origin_states_path: str
    forgery_states_path: str
    horizontal_sep: float
    vertical_sep: float

    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-o",
            "--output",
            help="Set output path",
            type=str,
            default="./output"
        )
        self.parser.add_argument(
            "-f",
            "--filter",
            help="Filter on a file path (must be exact), only matched " \
                "results will be included",
            type=str,
            default=""
        )
        self.parser.add_argument(
            "-d",
            "--dpi",
            help="Set the DPI for the image to generate (default is 100)",
            type=int,
            default=100
        )
        self.parser.add_argument(
            "-s",
            "--svg",
            help="Output in SVG format (default is png)",
            action="store_true"
        )
        self.parser.add_argument(
            "-O",
            "--origin-states",
            help="Specify the file to read the origin states from",
            type=str,
            default="origin-states.txt"
        )
        self.parser.add_argument(
            "-F",
            "--forgery-states",
            help="Specify the file to read the forgery states from",
            type=str,
            default="forgery-states.txt"
        )
        self.parser.add_argument(
            "-H",
            "--horizontal-sep",
            help="Specify the horizontal separation between columns " \
                "(default is 2)",
            type=float,
            default=2
        )
        self.parser.add_argument(
            "-V",
            "--vertical-sep",
            help="Specify the vertical separation between rows " \
                "(default is 0.5)",
            type=float,
            default=0.5
        )
        self.parser.add_argument("input", help="Input file path", type=str)

        args = self.parser.parse_args()
        self.input_path = args.input

        self.output_path, output_file = os.path.split(args.output)
        self.output_file = os.path.splitext(output_file)[0]
        self.filter = args.filter
        self.dpi = str(args.dpi)

        self.out_format = "png"
        if args.svg:
            self.out_format = "svg"

        self.origin_states_path = args.origin_states
        self.forgery_states_path = args.forgery_states
        self.horizontal_sep = str(args.horizontal_sep)
        self.vertical_sep = str(args.vertical_sep)
