""" This file contains some basic unit tests to make sure the
base functionality works correctly.
"""
from src.parser import Parser


class TestTimestampParser():

    def test_parse_operation_at_timestamp(self):
        operation = "(At 2020-OCTOBER-5 12:1:32.4338850 UTC: Access with last access update enabled)"
        expected = "<TIMESTAMP 2020-10-05T12:01:32.4338850 +0000 (At)>"
        actual = Parser.get_operation_timestamp(operation)
        assert actual == expected
    
    def test_parse_operation_between_timestamp(self):
        operation = "(Between 2020-OCTOBER-5 12:1:32.3446291 UTC and 2020-OCTOBER-5 12:1:35.3317866 UTC: Move in the same volume | File name change)"
        expected = "<TIMESTAMP 2020-10-05T12:01:32.3446291 +0000 - 2020-10-05T12:01:35.3317866 +0000 (Between)>"
        actual = Parser.get_operation_timestamp(operation)
        assert actual == expected

    def test_parse_operation_from_timestamp(self):
        operation = "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)"
        expected = "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 - 2020-10-05T12:02:44.6067758 +0000 (From)>"
        actual = Parser.get_operation_timestamp(operation)
        assert actual == expected

    def test_parse_operation_after_timestamp(self):
        operation = "(After 2020-OCTOBER-5 12:2:44.2437766 UTC: Delete)"
        expected = "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 (After)>"
        actual = Parser.get_operation_timestamp(operation)
        assert actual == expected


class TestOperationParser():

    def test_parse_operations(self):
        line = "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        expected = [
            "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
            "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        ]
        actual = Parser.get_operation_strings(line)
        assert actual == expected

    def test_parse_single_operation(self):
        line = "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)"
        expected = ["(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)"]
        actual = Parser.get_operation_strings(line)
        assert actual == expected

    def test_parse_MFT_operation(self):
        line = "0 .\$MFT (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"
        expected = ["(At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"]
        actual = Parser.get_operation_strings(line)
        assert actual == expected

    def test_parse_dot_operation(self):
        line = "5 . (At 2020-OCTOBER-5 12:3:31.4338850 UTC: Access with last access update enabled) <- (At 2020-OCTOBER-5 12:3:2.3646754 UTC: Update directory) <- (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"
        expected = [
            "(At 2020-OCTOBER-5 12:3:31.4338850 UTC: Access with last access update enabled)",
            "(At 2020-OCTOBER-5 12:3:2.3646754 UTC: Update directory)",
            "(At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"
        ]
        actual = Parser.get_operation_strings(line)
        assert actual == expected

    def test_parse_no_number_operation(self):
        line = ".\Folder\test2.odt (At 2020-OCTOBER-5 12:2:44.6067758 UTC: Overwriting move from another volume) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create with file tunneling | Update)"
        expected = [
            "(At 2020-OCTOBER-5 12:2:44.6067758 UTC: Overwriting move from another volume)",
            "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create with file tunneling | Update)"
        ]
        actual = Parser.get_operation_strings(line)
        assert actual == expected


class TestOperationActionParser:

    def test_operation_action_parser(self):
        operation = "(After 2020-OCTOBER-5 12:2:44.2437766 UTC: Delete)"
        expected = ["Delete"]
        actual = Parser.get_operation_actions(operation)
        assert actual == expected

    def test_multiple_actions(self):
        operation = "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create with file tunneling | Update)"
        expected = ["Create with file tunneling", "Update"]
        actual = Parser.get_operation_actions(operation)
        assert actual == expected

    def test_with_possibly_on_other_volume(self):
        operation = "(At 2020-OCTOBER-5 12:2:8.3062758 UTC: Copy | Copy with quirk) possibly on other volume"
        expected = ["Copy, possibly on other volume", "Copy with quirk, possibly on other volume"]
        actual = Parser.get_operation_actions(operation)
        assert actual == expected

    def test_with_on_other_volume(self):
        operation = "(At 2020-OCTOBER-5 12:2:8.3062758 UTC: Copy | Copy with quirk) on other volume"
        expected = ["Copy, on other volume", "Copy with quirk, on other volume"]
        actual = Parser.get_operation_actions(operation)
        assert actual == expected


class TestPathParser:

    def test_parse_path(self):
        line = "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        expected = ".\Folder\test2.odt"
        actual = Parser.get_file_path(line)
        assert actual == expected

    def test_parse_no_number_path(self):
        line = ".\Folder\test2.odt (At 2020-OCTOBER-5 12:2:44.6067758 UTC: Overwriting move from another volume) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create with file tunneling | Update)"
        expected = ".\Folder\test2.odt"
        actual = Parser.get_file_path(line)
        assert actual == expected

    def test_parse_mft_path(self):
        line = "0 .\$MFT (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"
        expected = ".\$MFT"
        actual = Parser.get_file_path(line)
        assert actual == expected

    def test_parse_dot_path(self):
        line = "5 . (At 2020-OCTOBER-5 12:3:31.4338850 UTC: Access with last access update enabled) <- (At 2020-OCTOBER-5 12:3:2.3646754 UTC: Update directory) <- (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)"
        expected = ""
        actual = Parser.get_file_path(line)
        assert actual == expected


class TestParseLine:

    def test_parse_line(self):
        line = "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        expected = (
            ".\\Folder\test2.odt",
            [
                (
                    "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                    " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                    "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 - 2020-10-05T12:02:44.6067758 +0000 (From)>",
                    ["Copy with file tunneling"],
                    "normal"
                ),
                (
                    "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                    " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                    "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                    [
                        "Create, possibly on other volume",
                        "Create with file tunneling, possibly on other volume"
                    ],
                    "origin"
                ),
                (
                    "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                    " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                    "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                    [
                        "Update, possibly on other volume",
                        "Update with last access update enabled, possibly on other volume"
                    ],
                    "normal"
                )
            ]
        )
        actual = Parser.parse_line(line, origin_states=["Create", "Create with file tunneling"])

        print(actual[0])
        for op in actual[1]:
            print("------------------------------------------")
            print(f"\t{op[0]}")
            print(f"\t{op[1]}")
            print(f"\t{op[2]}")
            print(f"\t{op[3]}")
            print(f"\t{op[4]}")

        assert actual == expected


class TestParseLines:

    def test_parse_lines(self):
        lines = [
            "0 .\$MFT (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
            "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        ]
        expected = [
            (
                ".\$MFT",
                [
                    (
                        "(At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
                        " <- (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
                        "<TIMESTAMP 2020-10-05T12:01:30.2715742 +0000 (At)>",
                        ["Create"],
                        "origin"
                    )
                ]
            ),
            (
                ".\\Folder\test2.odt",
                [
                    (
                        "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                        "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 - 2020-10-05T12:02:44.6067758 +0000 (From)>",
                        ["Copy with file tunneling"],
                        "normal"
                    ),
                    (
                        "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                        [
                            "Create, possibly on other volume",
                            "Create with file tunneling, possibly on other volume"
                        ],
                        "origin"
                    ),
                    (
                        "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                        [
                            "Update, possibly on other volume",
                            "Update with last access update enabled, possibly on other volume"
                        ],
                        "normal"
                    )
                ]
            )
        ]
        actual = Parser.parse_lines(lines, origin_states=["Create", "Create with file tunneling"])
        assert actual == expected

    def test_parse_lines_filter(self):
        lines = [
            "0 .\$MFT (At 2020-OCTOBER-5 12:1:30.2715742 UTC: Create)",
            "40 .\Folder\test2.odt (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume"
        ]
        expected = [
            (
                ".\\Folder\test2.odt",
                [
                    (
                        "(From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling)",
                        "<TIMESTAMP 2020-10-05T12:02:44.2437766 +0000 - 2020-10-05T12:02:44.6067758 +0000 (From)>",
                        ["Copy with file tunneling"],
                        "normal"
                    ),
                    (
                        "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                        [
                            "Create, possibly on other volume",
                            "Create with file tunneling, possibly on other volume"
                        ],
                        "origin"
                    ),
                    (
                        "(At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        " <- (From 2020-OCTOBER-5 12:2:44.2437766 UTC to 2020-OCTOBER-5 12:2:44.6067758 UTC: Copy with file tunneling) <- (At 2020-OCTOBER-5 12:2:37.4497311 UTC: Create | Create with file tunneling | Update | Update with last access update enabled) possibly on other volume",
                        "<TIMESTAMP 2020-10-05T12:02:37.4497311 +0000 (At)>",
                        [
                            "Update, possibly on other volume",
                            "Update with last access update enabled, possibly on other volume"
                        ],
                        "normal"
                    )

                ]
            )
        ]
        actual = Parser.parse_lines(lines, filter=".\\Folder\test2.odt",
            origin_states=["Create", "Create with file tunneling"])
        assert actual == expected      