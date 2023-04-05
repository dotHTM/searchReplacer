from __future__ import annotations
import re

from typing import Optional, Sequence

import subprocess
from time import sleep
import os

import platform

from searchReplacer.sed import SedCommand


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    sedExecPath = "sed"
    if platform.system() == "Darwin":
        sedExecPath = "gsed"

    sedWhich = subprocess.run(["which", sedExecPath], capture_output=True)
    assert sedWhich, "Can't find gnu-sed, is it installed? (brew gnu-sed)"

    def repoURL(path: str) -> str:
        return f"{host}:{path}"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sedCommand", type=str, default="./sedCommand", metavar="PATH"
    )
    parser.add_argument(
        "--repoFile",
        type=str,
        default="./repoList",
        metavar="PATH",
        help="A file containing a list of repository URLs to collect and act on. Overrides --repoList option.",
    )
    parser.add_argument(
        "--repoList",
        type=str,
        nargs="*",
        metavar="REPO_URL",
        help="List of repository URLs",
    )
    parser.add_argument(
        "--clearRepos",
        action="store_true",
        help="Remove the repos folder before doing work.",
    )
    parser.add_argument("--reposDir", type=str, default="repos", metavar="PATH")
    parser.add_argument(
        "--openCommand",
        type=str,
        default="",
        help="Command to open the repo with, such as `smerge` or `open`.",
        metavar="EXECUTABLE",
    )
    args = parser.parse_args(argv)

    if args.clearRepos and os.path.exists(args.reposDir):
        subprocess.run(["rm", "-rf", args.reposDir])
        sleep(2)

    if not args.repoList:
        with open(args.repoFile, "r") as f:
            args.repoList = f.read().split("\n")

    for url in args.repoList:
        searchResult = re.search(r"(?:[^:]*):(.*)", url)
        assert searchResult, "Had trouble reading the ssh git URL."
        repo = searchResult.groups()[0]

        myRepoDir = f"{args.reposDir}/{repo}"
        print(url, "->", myRepoDir)

        os.makedirs(myRepoDir, exist_ok=True)
        subprocess.run(["git", "clone", url, myRepoDir])
        subprocess.run(["git", "checkout", "-b", "find"])

        if args.openCommand:
            subprocess.run([args.openCommand, myRepoDir])

        filesRun = subprocess.run(
            ["grep", "-I", "-l", "-f", "grepCommand", "-r", myRepoDir],
            capture_output=True,
        )

        for file in filesRun.stdout.decode().split("\n"):
            print(file)
            sedRun = subprocess.run(
                [sedExecPath, "-i", "-f", "sedCommand", file],
                capture_output=True,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
