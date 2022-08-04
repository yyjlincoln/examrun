#!/usr/bin/python3


import license
import argv
import exam_scanner
import config
from globals import console
import time

# 10 minute buffer
BUFFER = 10 * 60


def main() -> None:
    print(f'ExamRun {license.VERSION}.')
    argv.check_revoke_license()
    license.confirm_license()
    argv.process_argv()
    cfg = config.read_config()
    console.line(1)
    console.print(f"Current exam: {cfg['title']}")
    print_current_time_and_deadline(cfg["deadline"], BUFFER)
    print_interval(time.time(), cfg["deadline"])
    if time.time() + BUFFER > cfg["deadline"]:
        console.print("[red]Buffered deadline is reached.[/red]")
        exit(1)

    files = config.parse_files_from_config(cfg)
    questions, missing_files = exam_scanner.scan(files)
    if len(missing_files.items()) != 0:
        console.print(
            '[red]Could not proceed with submission due to missing files\
.[/red]')
        raise FileNotFoundError()


def print_interval(fromT: int, toT: int):
    past = False
    if toT < fromT:
        past = True
        t = toT
        toT = fromT
        fromT = t
    diff = toT-fromT
    days = int(diff/(60*60*24))
    diff -= days * (60*60*24)
    hrs = int(diff/(60*60))
    diff -= hrs * (60*60)
    mins = int((diff)/60)
    diff -= mins*60
    seconds = int(diff)
    description = ""
    if days:
        description += f"{days} days, "
    if hrs:
        description += f"{hrs} hours, "
    if mins:
        description += f"{mins} mins, "
    if seconds:
        description += f"{seconds} seconds."
    if description.endswith(", "):
        description = description[:-2]
    description = description.strip()
    if past:
        print(f"This would be late by {description}")
    else:
        print(f"This would be early by {description}")


def print_current_time_and_deadline(deadline, buffer):
    print("Current time is " +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
          f" ({int(time.time())}).")
    print("Last time that examrun will give for you is " +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(deadline-buffer)) +
          f" ({deadline - buffer}).")
    print("The due date is " +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(deadline)) +
          f" ({deadline}).")


if __name__ == '__main__':
    try:
        main()
    except license.LicenseError:
        exit(1)
    except FileNotFoundError:
        exit(1)
    except config.ConfigDoesNotExistError:
        console.print("[red]Error: Config does not exist.[/red]")
        exit(1)
    except config.InvalidConfig:
        console.print("[red]Error: Invalid config.[/red]")
        exit(1)
