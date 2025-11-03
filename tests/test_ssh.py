import uuid

from .common import run_command, format_process_error
from .settings import get_host, get_user, get_private_key_path

HOST = get_host()
USER = get_user()
PRIVATE_KEY_PATH = get_private_key_path()


# TODO refactor ssh code to reduce repeating code
# TODO handle host key changed/unrecognized
# TODO port to paramiko?
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
