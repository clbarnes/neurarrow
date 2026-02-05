#!/usr/bin/env python3
import subprocess as sp
import datetime as dt
import sys
from typing import Literal
from argparse import ArgumentParser
from pathlib import Path
from difflib import unified_diff
import shlex

PROJECT_PATH = Path(__file__).resolve().parent
CHANGELOG_PATH = PROJECT_PATH.joinpath("src", "CHANGELOG.md")
UNRELEASED_SECTION = "## Unreleased"


def uncommitted_changes() -> str:
    res = sp.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return res.stdout.rstrip()


def get_version():
    res = sp.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        check=True,
        capture_output=True,
        text=True,
    )
    latest_tag = res.stdout.strip()
    return latest_tag.lstrip("v")


def bump_version(version: str, level: Literal["patch", "minor", "major"]):
    parts = [int(x) for x in version.split(".")][:3]

    while len(parts) < 3:
        parts.append(0)

    match level:
        case "patch":
            parts[2] += 1
        case "minor":
            parts[1] += 1
            parts[2] = 0
        case "major":
            parts[0] += 1
            parts[1] = 0
            parts[2] = 0
        case _:
            raise ValueError(f"Invalid level: {level}")

    return ".".join(str(x) for x in parts)


def commit_changes(execute=False):
    cmd = ["git", "commit", "-am", "Bump version in changelog"]
    if execute:
        sp.run(cmd, check=True)
    else:
        eprint(f"Would run: $ {shlex.join(cmd)}")


def tag_version(version: str, message: str, execute=False):
    tag_name = f"v{version}"
    cmd = ["git", "tag", "-a", tag_name, "-m", message]
    if execute:
        sp.run(cmd, check=True)
    else:
        eprint(f"Would run: $ {shlex.join(cmd)}")


def eprint(*args, **kwargs):
    kwargs.setdefault("file", sys.stderr)
    print(*args, **kwargs)


def update_changelog(new_version: str, message: str, execute=False):
    tag = f"v{new_version}"
    url = f"https://github.com/clbarnes/neurarrow/tree/{tag}"
    date = dt.date.today().isoformat()
    header = f"{UNRELEASED_SECTION}\n\n## [{new_version}]({url}) - {date}\n\n{message}"
    content = CHANGELOG_PATH.read_text()
    new_content = content.replace(UNRELEASED_SECTION, header)
    if execute:
        CHANGELOG_PATH.write_text(new_content)
    else:
        eprint("Would update CHANGELOG.md")
        print(
            "".join(
                unified_diff(
                    content.splitlines(True),
                    new_content.splitlines(True),
                    fromfile="before",
                    tofile="after",
                )
            )
        )


def main(raw_args: list[str] | None = None):
    parser = ArgumentParser(description="Bump the version of the project.")
    parser.add_argument(
        "level", choices=["patch", "minor", "major"], help="the level to bump"
    )
    parser.add_argument("message", help="the tag message for the version bump")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually create the tag (default: false)",
    )
    args = parser.parse_args(raw_args)

    if changes := uncommitted_changes():
        eprint(
            "Error: You have uncommitted changes. Please commit or stash them before bumping the version."
        )
        eprint(changes)
        sys.exit(1)

    latest_version = get_version()
    new_version = bump_version(latest_version, args.level)

    if not args.execute:
        eprint("Dry run: use --execute to enact changes")

    update_changelog(new_version, args.message, execute=args.execute)
    commit_changes(execute=args.execute)
    tag_version(new_version, args.message, execute=args.execute)


if __name__ == "__main__":
    main()
