#!/usr/bin/python3

import os
import typing as t
import license
from globals import console
import argv


def main() -> None:
    print(f'ExamRun {license.VERSION}.')
    argv.check_revoke_license()
    license.confirm_license()
    argv.process_argv()


if __name__ == '__main__':
    try:
        main()
    except license.LicenseError:
        exit(1)
