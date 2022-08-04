import sys
import license


def check_revoke_license():
    if len(sys.argv) == 1:
        return
    if sys.argv[1] == '--revoke-license':
        license.revoke_license()
        exit(0)
    raise Exception('Invalid argument')


def process_argv():
    if len(sys.argv) == 1:
        return
    if sys.argv[1] == '--revoke-license':
        license.revoke_license()
        exit(0)
    raise Exception('Invalid argument')
