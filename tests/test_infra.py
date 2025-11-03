import shlex
import subprocess
import uuid
from subprocess import CompletedProcess

import pytest
import requests

from .settings import get_host, get_user, get_private_key_path

HOST = get_host()
USER = get_user()
PRIVATE_KEY_PATH = get_private_key_path()


def run_command(command: str) -> CompletedProcess:
    split_command = shlex.split(command)
    return subprocess.run(split_command, capture_output=True)


def format_process_error(process: CompletedProcess, message: str) -> str:
    return message + (f"\nProcess info"
                      f"\nArgs: {process.args}"
                      f"\nReturn code: {process.returncode}"
                      f"\nStdout: {process.stdout.decode()}"
                      f"\nStderr: {process.stderr.decode()}")


@pytest.mark.parametrize("port", [22, 80])
def test_ports_are_open(port: int):
    timeout = 1
    proc = run_command(f"nc -z -w {timeout} {HOST} {port}")
    assert proc.returncode == 0, format_process_error(proc, f"Port {port} is not open")


def test_other_port_is_not_open():
    timeout = 1
    port = 8080
    proc = run_command(f"nc -z -w {timeout} {HOST} {port}")
    assert proc.returncode != 0, format_process_error(proc, f"Port {port} should not be open")


# TODO refactor ssh code to reduce repeating code
# TODO handle host key changed/unrecognized
def test_ssh_run_command():
    text = "Hello from the cloud!"
    proc = run_command(f"ssh -i {PRIVATE_KEY_PATH} {USER}@{HOST} echo {text}")
    assert text in proc.stdout.decode(), format_process_error(proc, f"Message '{text}' not found in output")


def test_ssh_upload_file(tmp_path):
    source = tmp_path / "test.txt"
    destination = f"/tmp/{uuid.uuid4()}.txt"
    text = "Hello from the cloud!"
    with open(source, "w") as f:
        f.write(text)

    proc = run_command(f"scp -i {PRIVATE_KEY_PATH} {source} {USER}@{HOST}:{destination}")
    assert proc.returncode == 0, format_process_error(proc, "Failed to upload file")

    proc = run_command(f"ssh -i {PRIVATE_KEY_PATH} {USER}@{HOST} cat {destination}")
    assert text in proc.stdout.decode(), format_process_error(proc, f"Message '{text}' not found in output")


def test_ssh_download_file(tmp_path):
    source = f"/tmp/{uuid.uuid4()}.txt"
    destination = tmp_path / "test.txt"
    text = "Hello from the cloud!"

    proc = run_command(f"ssh -i {PRIVATE_KEY_PATH} {USER}@{HOST} echo '{text}' >> {source}")
    assert proc.returncode == 0, format_process_error(proc, "Failed to create file in remote")

    proc = run_command(f"scp -i {PRIVATE_KEY_PATH} {USER}@{HOST}:{source} {destination}")
    assert proc.returncode == 0, format_process_error(proc, "Failed to download file")

    proc = run_command(f"cat {destination}")
    assert text in proc.stdout.decode(), format_process_error(proc, f"Message '{text}' not found in output")


def test_ssh_random_key_pair_does_not_work(tmp_path):
    random_key_path = tmp_path / "random.key"
    with open(random_key_path, "w") as f:
        f.write("password1234")

    text = "Hello from the cloud!"
    proc = run_command(f"ssh -i {random_key_path} {USER}@{HOST} echo {text}")
    assert proc.returncode != 0, format_process_error(proc, f"Command passed with random key")


def test_http_get():
    response = requests.get(f"http://{HOST}:80/")
    assert response.status_code == 200, (f"GET request failed. "
                                         f"Status code: {response.status_code}, "
                                         f"reason: {response.reason}, payload: {response.text}")
