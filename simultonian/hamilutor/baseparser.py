# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=too-many-instance-attributes,too-few-public-methods

"""Base class for Parser across frameworks"""
from typing import List, Tuple


class BaseParser:
    """
        Base class for Parser to parse different kinds of files and objects.
        The support for each file type and format is framework dependent.

        In general, parser does parsing from and to files. For example,
        parsing `.pauli` file into relevant format is possible in qiskit.
        Parser also encapsulates methods to convert circuits and other such
        objects to strings and by nature, files.

        =================
        Formats supported
        =================

        The format of the file is decided based on the extension of the file.
        Incorrect format will throw error.

        ---------------
         qiskit module
        ---------------
        - `.pauli`: Look at qiskit.parser for more details.
    """

    def __init__(self, framework: str) -> None:
        self.framework = framework
        self.formats: List[str] = []

    def base_parse(self, file_name: str) -> Tuple[str, str]:
        """Base parse the file
        Common parser that will be used by all the frameworks to read the file
        and return it's extension

        Args:
            file_name: Name of the file to be parsed.
        Raises:
            TypeError/AttributeError: Invalid file naming convention.
            NotImplementedError: File extension is not supported in the lib.
        """
        try:
            extension = file_name.split(".")[-1]

        except TypeError as err:
            raise TypeError(f"Invalid file name {file_name}, make sure that ",
                            "you have file with the correct naming ",
                            "convention.") from err
        except AttributeError as err:
            raise AttributeError(f"Invalid file name {file_name}, "
                                 "make sure that you have file with the",
                                 "correct naming convention.") from err

        if extension not in self.formats:
            raise NotImplementedError(
                f"format {extension} is not valid in {self.framework}.")

        string = ""
        with open(file_name, "r", encoding="utf-8") as file:
            string = file.read()

        return extension, string
