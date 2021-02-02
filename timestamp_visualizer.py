import json

from src.config import Config
from src.parser import Parser
from src.tree import generate_trees
from src.utils import read_states_file
from src.visualizer import Visualizer


if __name__ == "__main__":
    # Read command line arguments
    print("reading arguments...")
    config = Config()

    # Retrieve origin and forgery states
    print("retrieving origin and forgery states...")
    origin_states = read_states_file(config.origin_states_path)
    forgery_states = read_states_file(config.forgery_states_path)

    # Read and parse input file
    print("reading and parsing input input...")
    with open(config.input_path) as f:
        lines = f.readlines()
    parsed_lines = Parser.parse_lines(lines, origin_states=origin_states,
        filter=config.filter)

    # Generate file trees
    print("generating trees...")
    trees = generate_trees(parsed_lines)

    # Visualize trees
    print("Visualizing trees...")
    vis = Visualizer(
        trees=trees, 
        out_format=config.out_format,
        horizontal_sep=config.horizontal_sep,
        vertical_sep=config.vertical_sep,
        dpi=config.dpi,
        output_path = config.output_path,
        output_file = config.output_file,
        forgery_states=forgery_states
    )
    vis.visualize() 