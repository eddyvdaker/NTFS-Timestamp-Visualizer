from typing import List


def read_states_file(states_file_path: str) -> List[str]:
    """Read a states from file.

    :param states_file_path: the path to the txt file with origin states
    :return: a list of state operations
    """
    with open(states_file_path) as f :
        states = [l for l in f.read().split("\n")
            if "#" not in l[0:1] and l != ""]       # Read all non-comment and
                                                    # non-empty lines.
    return states 
