import pytest

from .common import run_command, format_process_error
from .settings import get_host, get_user, get_private_key_path

HOST = get_host()
USER = get_user()
PRIVATE_KEY_PATH = get_private_key_path()


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
