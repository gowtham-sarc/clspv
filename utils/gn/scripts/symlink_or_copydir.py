#!/usr/bin/env python3

"""Symlinks, or on Windows copies, an existing dir to a second location.

Overwrites the target location if it exists.
Updates the mtime on a stamp file when done."""

import argparse
import errno
import os
import sys
import glob


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stamp", required=True, help="name of a file whose mtime is updated on run"
    )
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()

    # FIXME: This should not check the host platform but the target platform
    # (which needs to be passed in as an arg), for cross builds.
    if sys.platform != "win32":
        for src in glob.glob("*/", root_dir=args.source):
            dst = os.path.join(args.output + os.path.dirname(src))
            print(f"Symlink for {src} in {dst}")

            try:
                os.makedirs(os.path.dirname(dst))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            try:
                os.symlink(os.path.join(args.source + src), dst)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.remove(dst)
                    os.symlink(os.path.join(args.source + src), dst)
                else:
                    raise
    else:
        import shutil

        output = args.output + ".exe"
        source = args.source + ".exe"
        shutil.copyfile(os.path.join(os.path.dirname(output), source), output)

    open(args.stamp, "w")  # Update mtime on stamp file.


if __name__ == "__main__":
    sys.exit(main())
