from __future__ import annotations
from typing import Generator, Optional, Sequence

import re

RegexMatchRegex = r"^([^/]*)/((?:\\/|[^/])+)/((?:\\/|[^/])+)/([^/]*)$"


class SedCommand:
    def __init__(self, operation, search, replace, options) -> None:
        self.operation = operation
        self.search = search
        self.replace = replace
        self.options = options

    def __repr__(self) -> str:
        operation = self.operation
        search = self.search
        replace = self.replace
        options = self.options

        return f"{type(self).__name__}({operation=}, {search=}, {replace=}, {options=})"

    @classmethod
    def fromRegEx(cls, regexString: str):
        matchResults = re.match(RegexMatchRegex, regexString)
        assert matchResults
        mrg = list(matchResults.groups())
        assert 4 == len(mrg)
        return cls(*mrg)

    @classmethod
    def readFile(cls, path) -> Generator:
        with open(path, "r") as f:
            for line in f.read().split("\n"):
                if line:
                    yield cls.fromRegEx(line)

    @classmethod
    def writeGrepFile(cls, inFile, outFile):
        with open(outFile, "w") as f:
            grepBuffer = []
            for c in cls.readFile(inFile):
                grepBuffer.append(c.search)
            f.write("\n".join(grepBuffer))


def main(argv: Optional[Sequence[str]] = None) -> int:
    import os

    os.remove("grepCommand")
    SedCommand.writeGrepFile("sedCommand", "grepCommand")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
