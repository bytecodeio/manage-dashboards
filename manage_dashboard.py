import argparse
from os import path
import json
from commands import new, develop, deploy, status, update, rollback, delete, rename
from utils import git_repo
from utils import parse_ini

base_url = "https://bytecodeef.looker.com"
loc = "looker.ini"


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    setup_new_subparser(subparsers)
    setup_develop_subparser(subparsers)
    setup_deploy_subparser(subparsers)
    setup_update_subparser(subparsers)
    setup_rollback_subparser(subparsers)
    setup_delete_subparser(subparsers)
    setup_rename_subparser(subparsers)
    setup_status_subparser(subparsers)
    args = parser.parse_args()
    repo = git_repo.init_repo(args.ini, args.env)
    ini = parse_ini.read_ini(args.ini)
    config = ini[args.env]
    catalog_file = config["catalog_file"]

    if path.exists(catalog_file):
        pass
    else:
        catalog = {}
        with open(catalog_file, 'w+') as catfile:
            json.dump(catalog, catfile)
    try:
        args.func(args, catalog_file, repo)
    except AttributeError as err:
        print(err)
        parser.print_help()
        parser.exit(1)


def setup_new_subparser(subparsers):
    new_subparser = subparsers.add_parser("new")
    new_subparser.add_argument("--name", required=True,  help="name of new dashboard to create or update")
    new_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    new_subparser.add_argument("--env", required=True, help="what environment to interact with")
    new_subparser.add_argument("--target_folder", default='Development', help="folder to create in")
    new_subparser.add_argument("--version", required=True, help="new dashboard version")
    new_subparser.set_defaults(func=new.main)


def setup_develop_subparser(subparsers):
    develop_subparser = subparsers.add_parser("develop")
    develop_subparser.add_argument("--name", required=True, help="name of dashboard to develop")
    develop_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    develop_subparser.add_argument("--env", required=True, help="what environment to interact with")
    develop_subparser.add_argument("--target_folder", default='Development', help="folder to develop from")
    develop_subparser.add_argument("--source_folder", default='Production', help="folder to develop in")
    develop_subparser.add_argument("--version", required=True, help="new dashboard version")
    develop_subparser.set_defaults(func=develop.main)


def setup_deploy_subparser(subparsers):
    deploy_subparser = subparsers.add_parser("deploy")
    deploy_subparser.add_argument("--name", required=True, help="name of dashboard to deploy")
    deploy_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    deploy_subparser.add_argument("--env", required=True, help="what environment to interact with")
    deploy_subparser.add_argument("--target_folder", default='Development', help="folder to deploy to")
    deploy_subparser.add_argument("--source_folder", default='Production', help="folder to deploy from")
    deploy_subparser.add_argument("--version", required=True, help="new dashboard version")
    deploy_subparser.set_defaults(func=deploy.main)

def setup_update_subparser(subparsers):
    update_subparser = subparsers.add_parser("update")
    update_subparser.add_argument("--name", required=True, help="name of dashboard to update")
    update_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    update_subparser.add_argument("--env", required=True, help="what environment to interact with")
    update_subparser.add_argument("--source_folder", default='Development', help="folder to update from")
    update_subparser.add_argument("--version", required=True, help="new dashboard version")
    update_subparser.set_defaults(func=update.main)

def setup_rollback_subparser(subparsers):
    rollback_subparser = subparsers.add_parser("rollback")
    rollback_subparser.add_argument("--name", required=True, help="name of dashboard to rollback")
    rollback_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    rollback_subparser.add_argument("--env", required=True, help="what environment to interact with")
    rollback_subparser.add_argument("--source_folder", default='Development', help="folder to rollback dashboard in")
    rollback_subparser.set_defaults(func=rollback.main)

def setup_rename_subparser(subparsers):
    rename_subparser = subparsers.add_parser("rename")
    rename_subparser.add_argument("--name", required=True, help="name of dashboard to rename")
    rename_subparser.add_argument("--new_name", required=True, help="new name for dashboard")
    rename_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    rename_subparser.add_argument("--env", required=True, help="what environment to interact with")
    rename_subparser.add_argument("--source_folder", default='Development', help="folder in which to rename dashboard")
    rename_subparser.add_argument("--version", required=True, help="new dashboard version")
    rename_subparser.set_defaults(func=rename.main)

def setup_delete_subparser(subparsers):
    delete_subparser = subparsers.add_parser("delete")
    delete_subparser.add_argument("--name", required=True, help="name of dashboard to delete")
    delete_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    delete_subparser.add_argument("--env", required=True, help="what environment to interact with")
    delete_subparser.add_argument("--source_folder", default='Development', help="folder to delete dashboard in")
    delete_subparser.add_argument("--archive_folder", default='Archive', help="folder to archive dashboard in")
    delete_subparser.add_argument("--archive", default=False, help="should dashboard be archived")
    delete_subparser.add_argument("--version", required=False, help="dashboard version if archiving")
    delete_subparser.set_defaults(func=delete.main)

def setup_status_subparser(subparsers):
    status_subparser = subparsers.add_parser("status")
    status_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    status_subparser.add_argument("--env", required=True, help="what environment to interact with")
    status_subparser.set_defaults(func=status.main)


if __name__ == "__main__":
    main()
