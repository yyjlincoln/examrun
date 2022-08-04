import sys
import license
from globals import console


def check_revoke_license():
    if len(sys.argv) == 1:
        return
    if sys.argv[1] == '--revoke-license':
        license.revoke_license()
        exit(0)
    if sys.argv[1] == '--accept-license':
        console.print('[green]Accepted license (--accept-license).[/green]')
        license.persist_license()
        return

    raise Exception('Invalid argument')


def process_argv():
    if len(sys.argv) == 1:
        return
    if sys.argv[1] == '--revoke-license':
        license.revoke_license()
        exit(0)
