from utils import parse_ini
import subprocess
import os


def export(args, folder_id):
    git_ini = parse_ini.read_ini(args.ini)
    git_config = git_ini[args.env]
    local_git_dir = git_config["local_git_dir"]
    ldeploy_command = [
        "ldeploy",
        "content",
        "export",
        "--env",
        args.env,
        "--ini",
        args.ini,
        "--folders",
        folder_id,
        "--local-target",
        local_git_dir
    ]
    if os.name == "nt":
        win_exec = ["cmd.exe", "/c"]
        ldeploy_command = win_exec + ldeploy_command

    subprocess.run(ldeploy_command)
