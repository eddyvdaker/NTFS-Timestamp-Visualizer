"""
    src.Parser
    ==========
    This file contains the code required to parse the input file.


    Output format:
    --------------
    [
        (
            {{ file }},
            [
                (
                    {{ operation_string }},
                    {{ timestamp }},
                    [{{ action }}, {{ action }}, ...]
                ),
                ...
            ]
        ),
        ...
    ]

    Example input:
    --------------
    [
        "0 .\$MFT (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
        "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
    ]

    Example output:
    ---------------
    [
        (
            ".\$MFT",
            [
                (
                    "(At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
                    "<TIMESTAMP 2020-10-05T12:01:30.2715742 +0000 (At)>",
                    ["Create"]
                )
            ]
        ),
        (
            ".\\Folder\test2.odt",
            [
                (
                    "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                    "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 - 2020-10-05T12:02:44.6067758 +0000 (From)>",
                    ["Copy with file tunneling"]
                ),
                (
                    "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                    "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                    [
                        "Create, possibly on other volume",
                        "Create with file tunneling, possibly on other volume",
                        "Update, possibly on other volume",
                        "Update with last access update enabled, possibly on other volume"
                    ]
                )
            ]
        )
    ]

"""

import re
from dateutil.parser import parse as dateutil_parse
from typing import List, Tuple

from src.config import Config

# Regex to extract the operations from a line. In order it checks for the
# following:
# - Check for At|From|Between|After
# - Check for either one or two timestamps (YYYY-M-D H:M:S.ns formatting)
# - Check for operation text
# - Check for optional "possibly on other volume" or "on other volume" ending 
ops_regex = re.compile(
    "\((At|From|Between|After) " +
    "([0-9]{4}-[A-Z]+-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}.[0-9]+ " +
    "[A-Z]+(:| and | to )){1,2} " +
    "[A-Za-z \| \-]+\)( possibly on other volume| on other volume)?")

# Regex to check of which type the timestamp is (At|From|Between|After)
timestamp_type_regex = re.compile("At|From|Between|After")

# Regex to retrieve the timestamp itself (YYYY-M-D H:M:S.ns formatting)
timestamp_regex = re.compile(
    "[0-9]{4}-[A-Z]+-[0-9]{1,2} " +
    "[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}.[0-9]+ " +
    "[A-Z]+")


class ParserException(BaseException):
    """Custom exception for parser errors."""
    pass


class Parser(object):
    """The Parser class provides serveral (static) methods for
    extracting data from the TimeStampAnalyser. 
    """

    @staticmethod
    def get_operation_strings(line: str) -> List[str]:
        """Parse the operation strings from a line.

        :param line: the line to parse
        :return: a list of operation strings
        """
        operations = []
        for op in ops_regex.finditer(line):
            operations.append(op.group(0))
        return operations

    @staticmethod
    def get_operation_actions(operation: str) -> List[str]:
        """Parse the operation actions from an operation.

        :param operation: the operation to get the actions from
        :return: the actions in this operation        
        """
        actions = []

        # split 
        action_strings = operation.split("|")
        action_strings[0] = action_strings[0].split(":")[-1]

        # add "(possibly) on other volume to actions when needed"
        add_to_end = ""
        if action_strings[-1].endswith(") possibly on other volume"):
            action_strings[-1] = action_strings[-1]\
                .replace(") possibly on other volume", "")
            add_to_end = ", possibly on other volume"
        elif action_strings[-1].endswith(") on other volume"):
            action_strings[-1] = action_strings[-1]\
                .replace(") on other volume", "")
            add_to_end= ", on other volume"
        else:
            action_strings[-1] = action_strings[-1].replace(")", "")
        
        for action in action_strings:
            action = action.strip()
            action += add_to_end
            actions.append(action)
        return actions

    @staticmethod
    def get_file_path(line: str) -> str:
        """Parse the file path from a line.

        :param line: the line to parse
        :return: the path of the line
        """
        path_start_index = line.find(".\\")
        # -1 to remove the space before after the file path
        path_end_index = line.find(ops_regex.search(line).group()) - 1
        return line[path_start_index:path_end_index]

    @staticmethod
    def get_operation_timestamp(operation: str) -> str:
        """Extract the timestamp from the operation.

        :param operation: the operation to extract the timestamp from
        :return: the timestamp
        """
        def format_timestamp(timestamp: str) -> str:
            dt = dateutil_parse(timestamp)
            formatted_ts = f"{dt.year}-{dt.month:02d}-{dt.day:02d}"
            formatted_ts += f"T{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

            last_digit = timestamp.split(".")
            last_digit = last_digit[1]
            last_digit = last_digit.split(" ")
            last_digit = last_digit[0]
            last_digit = last_digit[-1]

            formatted_ts += f".{dt.microsecond:06d}{last_digit}"
            formatted_ts += f" {dt.strftime('%z')}"
            return formatted_ts 
        timestamp_type = timestamp_type_regex.search(operation).group()
        matches = timestamp_regex.findall(operation)
        formatted_timestamp = f"<TIMESTAMP {format_timestamp(matches[0])}"
        if len(matches) == 2:
            formatted_timestamp += f" - {format_timestamp(matches[1])}"
        formatted_timestamp += f" ({timestamp_type})>"
        return formatted_timestamp

    @staticmethod
    def parse_line(line: str, line_no: int = None,
            origin_states: List[str] = []) -> Tuple[str, List]:
        """Parse an entire line.

        :param line: the line to parse
        :return: the file path and the operations in the line
        """
        filepath = Parser.get_file_path(line)
        timestamp_operation_list = []
        previous_path = ""
        for operation in Parser.get_operation_strings(line):
            timestamp = Parser.get_operation_timestamp(operation)
            actions = Parser.get_operation_actions(operation)
            normal_actions = []
            origin_actions = []

            for action in actions:
                # Remove "(possibly) on other volume", because initial states
                # are given without this included
                action_str = action\
                    .replace(", possibly on other volume", "")\
                    .replace(", on other volume", "")
                if action_str in origin_states:
                    origin_actions.append(action)
                else:
                    normal_actions.append(action)
            path = f"{previous_path} <- {operation}"
            if origin_actions:
                timestamp_operation_list.append((
                    operation,          # Operation String
                    path,               # Operations Path 
                    timestamp,          # Timestamp
                    origin_actions,     # Actions (list)
                    "origin"            # Operation type (origin)
                ))
            if normal_actions:
                timestamp_operation_list.append((
                    operation,          # Operation String
                    path,               # Operations Path 
                    timestamp,          # Timestamp
                    normal_actions,     # Actions (list)
                    "normal"            # Operation type (normal)
                ))
                previous_path = path

        return (filepath, timestamp_operation_list)

    @staticmethod
    def parse_lines(lines: List[str], origin_states: List[str] = [],
            filter: str = "") -> List:
        """Parse the an TimeStampAnalyser output file.

        :param lines: list of lines
        :param filter: only parse lines that match the filter
        :return: list of parsed lines
        """
        parsed_lines = []
        for num, line in enumerate(lines):
            if filter in line:
                parsed_lines.append(Parser.parse_line(line, line_no=num,
                    origin_states=origin_states))
        return parsed_lines
        