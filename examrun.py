#!/usr/bin/python3

import license
import argv
import exam_scanner


def main() -> None:
    print(f'ExamRun {license.VERSION}.')
    argv.check_revoke_license()
    license.confirm_license()
    argv.process_argv()
    exam_scanner.initialise()


if __name__ == '__main__':
    try:
        main()
    except license.LicenseError:
        exit(1)
