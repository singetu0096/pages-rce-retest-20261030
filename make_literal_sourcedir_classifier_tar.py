#!/usr/bin/env python3
import io
import tarfile


# If passed through a shell without escaping, the quote terminates the intended
# argument, ':' is a no-op shell builtin, and '#' comments out the remainder.
# If passed safely as one literal argument, pages-untar should publish the file.
source_dir = "q';:;#"
marker = b"PAGES_RETEST_LITERAL_SOURCEDIR_SAFE_20261030\n"

with tarfile.open(
    "pages-retest-literal-sourcedir.tar", "w", format=tarfile.USTAR_FORMAT
) as archive:
    directory = tarfile.TarInfo(source_dir)
    directory.type = tarfile.DIRTYPE
    directory.mode = 0o755
    directory.mtime = 0
    archive.addfile(directory)

    page = tarfile.TarInfo(f"{source_dir}/index.html")
    page.mode = 0o644
    page.mtime = 0
    page.size = len(marker)
    archive.addfile(page, io.BytesIO(marker))

with tarfile.open("pages-retest-literal-sourcedir.tar") as archive:
    members = archive.getmembers()

assert [member.name for member in members] == [source_dir, f"{source_dir}/index.html"]
assert members[0].isdir()
assert members[1].isfile()
