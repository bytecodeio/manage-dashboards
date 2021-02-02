from utils import parse_ini
from git import Repo
from os import path
import git


def init_repo(ini, env):
    git_ini = parse_ini.read_ini(ini)
    git_config = git_ini[env]
    git_token = git_config["git_token"]
    git_base = git_config["git_base"]
    git_url = f"https://{git_token}:x-oauth-basic@{git_base}"
    local_git_dir = git_config["local_git_dir"]
    try:
        repo = Repo(path.join(local_git_dir))
        repo.remotes.origin.pull('master')
        repo.config_writer().set_value('user', 'name', git_config["git_user"]).release()
        repo.config_writer().set_value('user', 'email', git_config["git_email"]).release()
    except git.exc.NoSuchPathError:
        print("Specified local git directory does not exist.  Attempting to clone...")
        repo = Repo.clone_from(git_url, local_git_dir)
        repo.config_writer().set_value('user', 'name', git_config["git_user"]).release()
        repo.config_writer().set_value('user', 'email', git_config["git_email"]).release()
        print(f"Repository cloned on branch {repo.active_branch}")
    except git.exc.GitCommandError as err:
        print(err)
    except Exception as err:
        print(err)
    return repo


def write_to_repo(repo, commit_message):
    has_changed = False
    for file in repo.untracked_files:
        print(f'Added untracked file: {file}')
        repo.git.add(file)
        if has_changed is False:
            has_changed = True
    if repo.is_dirty() is True:
        for file in repo.git.diff(None, name_only=True).split('\n'):
            if len(file) < 1:
                continue
            print(f'Added file: {file}')
            repo.git.add(file)
            if has_changed is False:
                has_changed = True
    if has_changed is True:
        repo.git.commit('-m', commit_message)
        repo.git.push('origin', 'master')
        print(commit_message)
    sha = repo.head.object.hexsha
    return sha


def checkout_commit(ini, env, commit, temp_git_dir):
    git_ini = parse_ini.read_ini(ini)
    git_config = git_ini[env]
    git_url = "https://{}:x-oauth-basic@{}".format(git_config["git_token"], git_config["git_base"])
    if path.exists(temp_git_dir):
        print("Temp directory {} already exists for cloning of specific commit".format(temp_git_dir))
        exit(1)
    repo = Repo.clone_from(git_url, temp_git_dir, no_checkout=True)
    repo.git.checkout(commit)
    return repo
