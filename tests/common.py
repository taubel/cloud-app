import shlex
import subprocess
from subprocess import CompletedProcess


def run_command(command: str) -> CompletedProcess:
    split_command = shlex.split(command)
    return subprocess.run(split_command, capture_output=True)


def format_process_error(process: CompletedProcess, message: str) -> str:
    return message + (f"\nProcess info"
                      f"\nArgs: {process.args}"
                      f"\nReturn code: {process.returncode}"
                      f"\nStdout: {process.stdout.decode()}"
                      f"\nStderr: {process.stderr.decode()}")
