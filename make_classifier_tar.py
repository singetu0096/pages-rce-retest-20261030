#!/usr/bin/env python3
import io
import tarfile


marker = b"PAGES_RETEST_RAW_ARTIFACT_CLASSIFIER_20261030\n"

with tarfile.open("pages-retest-classifier.tar", "w", format=tarfile.USTAR_FORMAT) as archive:
    directory = tarfile.TarInfo("artifact-root")
    directory.type = tarfile.DIRTYPE
    directory.mode = 0o755
    directory.mtime = 0
    archive.addfile(directory)

    page = tarfile.TarInfo("artifact-root/index.html")
    page.mode = 0o644
    page.mtime = 0
    page.size = len(marker)
    archive.addfile(page, io.BytesIO(marker))

with tarfile.open("pages-retest-classifier.tar") as archive:
    members = archive.getmembers()

assert [member.name for member in members] == ["artifact-root", "artifact-root/index.html"]
assert members[0].isdir()
assert members[1].isfile()
