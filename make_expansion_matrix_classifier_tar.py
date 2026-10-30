#!/usr/bin/env python3
import io
import tarfile


# Classify two shell-expansion families in one bounded deployment. Backtick
# command substitution executes only the printf builtin. The parameter form
# tests whether the standard IFS parameter is set but never exposes its value.
literal_dir = "mix`printf B`${IFS:+V}"
backtick_only_dir = "mixB${IFS:+V}"
parameter_only_dir = "mix`printf B`V"
both_expanded_dir = "mixBV"

cases = [
    (literal_dir, b"PAGES_RETEST_EXPANSION_LITERAL_SAFE_20261030\n"),
    (backtick_only_dir, b"PAGES_RETEST_BACKTICK_ONLY_EXECUTED_20261030\n"),
    (parameter_only_dir, b"PAGES_RETEST_PARAMETER_ONLY_EXPANDED_20261030\n"),
    (both_expanded_dir, b"PAGES_RETEST_BOTH_EXPANSIONS_EXECUTED_20261030\n"),
]


def add_directory(archive: tarfile.TarFile, name: str) -> None:
    directory = tarfile.TarInfo(name)
    directory.type = tarfile.DIRTYPE
    directory.mode = 0o755
    directory.mtime = 0
    archive.addfile(directory)


def add_page(archive: tarfile.TarFile, directory: str, body: bytes) -> None:
    page = tarfile.TarInfo(f"{directory}/index.html")
    page.mode = 0o644
    page.mtime = 0
    page.size = len(body)
    archive.addfile(page, io.BytesIO(body))


output = "pages-retest-expansion-matrix.tar"
with tarfile.open(output, "w", format=tarfile.USTAR_FORMAT) as archive:
    for directory, marker in cases:
        add_directory(archive, directory)
        add_page(archive, directory, marker)

with tarfile.open(output) as archive:
    members = archive.getmembers()

expected = []
for directory, _marker in cases:
    expected.extend([directory, f"{directory}/index.html"])

assert [member.name for member in members] == expected
assert all(members[index].isdir() for index in range(0, len(members), 2))
assert all(members[index].isfile() for index in range(1, len(members), 2))
