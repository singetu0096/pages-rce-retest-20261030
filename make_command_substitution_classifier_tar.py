#!/usr/bin/env python3
import io
import tarfile


# This is a side-effect-free shell-serialization classifier. If SourceDir is
# safely transported as literal data, the first marker is published. If it is
# placed in double quotes (or left unquoted), the shell evaluates only the
# printf builtin and SourceDir becomes the second directory, selecting the
# second marker. No file write, network request, secret read, or external
# command is performed by the substitution itself.
literal_dir = "subst$(printf X)"
expanded_dir = "substX"
literal_marker = b"PAGES_RETEST_SUBST_LITERAL_SAFE_20261030\n"
expanded_marker = b"PAGES_RETEST_SUBST_EXPANDED_EXECUTED_20261030\n"


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


with tarfile.open(
    "pages-retest-command-substitution.tar", "w", format=tarfile.USTAR_FORMAT
) as archive:
    add_directory(archive, literal_dir)
    add_page(archive, literal_dir, literal_marker)
    add_directory(archive, expanded_dir)
    add_page(archive, expanded_dir, expanded_marker)

with tarfile.open("pages-retest-command-substitution.tar") as archive:
    members = archive.getmembers()

assert [member.name for member in members] == [
    literal_dir,
    f"{literal_dir}/index.html",
    expanded_dir,
    f"{expanded_dir}/index.html",
]
assert members[0].isdir() and members[1].isfile()
assert members[2].isdir() and members[3].isfile()
