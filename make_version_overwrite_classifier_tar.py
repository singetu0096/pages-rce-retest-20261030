#!/usr/bin/env python3
"""Create a bounded tar that classifies pages-build-version overwrite mode."""

import io
import tarfile


directory = "pbv-overwrite-classifier"
marker = b"PAGES_RETEST_VERSION_OVERWRITE_CLASSIFIER_20261030\n"
# A successful deployment overwrites the beginning with its trusted revision.
# Any remaining B bytes demonstrate an in-place write without truncation.
seed_version = b"B" * 128
output = "pages-retest-version-overwrite.tar"


def add_file(archive: tarfile.TarFile, name: str, body: bytes) -> None:
    item = tarfile.TarInfo(name)
    item.mode = 0o644
    item.mtime = 0
    item.size = len(body)
    archive.addfile(item, io.BytesIO(body))


with tarfile.open(output, "w", format=tarfile.USTAR_FORMAT) as archive:
    root = tarfile.TarInfo(directory)
    root.type = tarfile.DIRTYPE
    root.mode = 0o755
    root.mtime = 0
    archive.addfile(root)
    add_file(archive, f"{directory}/index.html", marker)
    add_file(archive, f"{directory}/pages-build-version", seed_version)

with tarfile.open(output) as archive:
    members = archive.getmembers()

assert [(item.name, item.type, item.size) for item in members] == [
    (directory, tarfile.DIRTYPE, 0),
    (f"{directory}/index.html", tarfile.REGTYPE, len(marker)),
    (f"{directory}/pages-build-version", tarfile.REGTYPE, len(seed_version)),
]
