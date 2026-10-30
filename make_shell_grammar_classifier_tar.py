#!/usr/bin/env python3
import io
import tarfile


# Exercise shell grammar not covered by the earlier quote/substitution matrix:
# whitespace, CR/LF, double quote, backslash, arithmetic and ANSI-C expansion,
# process substitution, brace/glob syntax, control operators, and parentheses.
# The process-substitution body is only the shell builtin `printf` and has no
# external side effect. A correctly quoted SourceDir publishes the fixed marker.
literal_dir = "meta \t~*?[x]{L,R}\"\\$((1+1))$'A'<(printf P)&|()!\r\nEND"
marker = b"PAGES_RETEST_META_GRAMMAR_LITERAL_SAFE_20261030\n"


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


output = "pages-retest-shell-grammar.tar"
with tarfile.open(output, "w", format=tarfile.USTAR_FORMAT) as archive:
    add_directory(archive, literal_dir)
    add_page(archive, literal_dir, marker)

with tarfile.open(output) as archive:
    members = archive.getmembers()

assert [member.name for member in members] == [
    literal_dir,
    f"{literal_dir}/index.html",
]
assert members[0].isdir()
assert members[1].isfile()

