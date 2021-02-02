import subprocess
import os


def import_dash(filename, args, target_folder):
    if os.name == "nt":
        target_folder = "Shared\\" + target_folder
    else:
        target_folder = "Shared/" + target_folder
    ldeploy_command = [
        "ldeploy",
        "content",
        "import",
        "--env",
        args.env,
        "--ini",
        args.ini,
        "--target-folder",
        target_folder,
        "--dashboard",
        filename
    ]
    print(ldeploy_command)
    if os.name == "nt":
        win_exec = ["cmd.exe", "/c"]
        ldeploy_command = win_exec + ldeploy_command

    subprocess.run(ldeploy_command)
    return
