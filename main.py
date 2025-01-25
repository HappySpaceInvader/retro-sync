import toml
import subprocess

config = toml.load("config.toml")
REMOTE = config["paths"]["remote"]
LOCAL = config["paths"]["local"]

def download_saves():
    rsync_command = [
        "rsync",
        "-avz",
        REMOTE,
        LOCAL
    ]
    subprocess.run(rsync_command, check=True)

def upload_saves():
    rsync_command = [
        "rsync",
        "-avz",
        "--update",  # Skip files that are newer on the receiver
        LOCAL,
        REMOTE
    ]
    subprocess.run(rsync_command, check=True)

def sync_saves():
    download_saves()
    upload_saves()

