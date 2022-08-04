import sys
from globals import console
from rich import box
from rich.table import Table
import os

VERSION: str = "v0.1.0"

LICENSE: str = '''
Copyright (C) 2022 Lincoln Yan.

The use of this software is generally governed by the MIT license, \
with additional conditions outlined below:

You are reminded of the importance of academic integrity, and you agree \
that you will only use this software in a way that respects the relevant \
requirements of the assessable work and the policies of the university.

You agree that the authors/contributors of this software must not be held \
liable for any damages that may result from your use of this software, \
for example, being involved in an academic integrity investigation.

This software is distributed in good faith and hope to be useful, but \
without any warranty, implied or otherwise. You must check the submissions \
yourself to ensure the submission is valid.

By using this software, you agree to the above conditions.
'''


def print_license() -> None:
    """Print the license."""
    table = Table(header_style="bold", box=box.ASCII2)
    table.add_column("License")
    table.add_row(LICENSE)
    console.print(table)


FULL_LICENSE = '''
Copyright (C) 2022 Lincoln Yan.

Permission is hereby granted, free of charge, \
to any person obtaining a copy of this software \
and associated documentation files (the "Software"),\
to deal in the Software without restriction, \
including without limitation the rights to use, \
copy, modify, merge, publish, distribute, sublicense, \
and/or sell copies of the Software, and to permit \
persons to whom the Software is furnished to do so, \
subject to the following conditions:

The above copyright notice and this permission notice \
shall be included in all copies or substantial portions \
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY \
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE \
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS \
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR \
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT \
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH \
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\

Additional conditions:

You are reminded of the importance of academic integrity, and you agree \
that you will only use this software in a way that respects the relevant \
requirements of the assessable work and the policies of the university.

You agree that the authors/contributors of this software must not be held \
liable for any damages that may result from your use of this software, \
for example, being involved in an academic integrity investigation.

This software is distributed in good faith and hope to be useful, but \
without any warranty, implied or otherwise. You must check the submissions \
yourself to ensure the submission is valid.

'''.strip()


def get_persisted_license_location() -> str:
    return os.path.join(os.path.expanduser('~'), '.examrun.license')


def check_persisted_license_status() -> bool:
    if not os.path.exists(get_persisted_license_location()) or \
            not os.path.isfile(get_persisted_license_location()):
        return False

    with open(get_persisted_license_location(), 'r') as f:
        if f.read().strip() == FULL_LICENSE:
            return True

    return False


def persist_license() -> None:
    with open(get_persisted_license_location(), 'w') as f:
        f.write(FULL_LICENSE)


def confirm_license() -> None:
    if check_persisted_license_status():
        console.print(
            "[green]You've previously agreed to the license.[/green]")
        console.print(
            f"[green]You can delete [blue]{get_persisted_license_location()}[/blue] \
or run [blue]{sys.argv[0]} --revoke-license[/blue] to revoke.[/green]")
        return
    console.clear()
    print(f"ExamRun {VERSION}.")
    print_license()
    try:
        i = input("Please confirm the above license (Y/n): ")
    except KeyboardInterrupt:
        console.print('')
        console.print("[red]License not accepted.[/red]")
        exit(1)
    except EOFError:
        console.print('')
        console.print("[red]License not accepted.[/red]")
        exit(1)

    if i.lower() == "y" or i == '':
        console.clear()
        print(f"ExamRun {VERSION}.")
        console.print('[green]License accepted.[/green]')
        persist_license()
        return
    console.print('[red]License not accepted.[/red]')
    raise LicenseError()


class LicenseError(Exception):
    '''Raised when the license is not accepted.'''
    pass


def revoke_license():
    if not check_persisted_license_status():
        console.print('[red]License not found.[/red]')
        return
    os.remove(get_persisted_license_location())
    console.print('[green]License revoked.[/green]')
    return
