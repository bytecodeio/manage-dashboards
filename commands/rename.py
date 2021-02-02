import json
from utils.get_client import get_client
from utils import export_dash, find_file, git_repo, parse_ini
import looker_sdk
import os


def main(args, catalog_file, repo):
    ini = parse_ini.read_ini(args.ini)
    config = ini[args.env]
    local_git_dir = config["local_git_dir"]
    sdk = get_client(args.ini, args.env)
    folder_results = sdk.search_folders(name=args.source_folder)

    if len(folder_results) == 0:
        print(f"{args.source_folder} folder does not exist")
        exit(1)
    else:
        folder_id = folder_results[0].id

    results = sdk.search_dashboards(title=args.name, folder_id=folder_id)

    if len(results) == 0:
        print(f"Dashboard {args.name} not found in folder {args.source_folder}")
        exit(1)
    elif len(results) == 1:
        dash_id = results[0].id
        with open(catalog_file, 'r+') as catfile:
            catalog = json.load(catfile)
        if args.source_folder not in catalog.keys():
            catalog[args.source_folder] = []
        dash_index = next((i for i, dash in enumerate(catalog[args.source_folder]) if dash['id'] == dash_id), None)
        if dash_index is None:
            print(f"{args.name} does not exist in catalog file, did you mean to update?")
            exit(0)

        filename = find_file.get_filename(local_git_dir, dash_id, args.source_folder)
        try:
            os.remove(filename)
            git_repo.write_to_repo(repo, f"Removed dashboard {args.name} from folder {args.source_folder}")
        except OSError as err:
            print(f"Error: {local_git_dir} : {err}")

        dashboardobject = looker_sdk.models.WriteDashboard(
            title=args.new_name
        )
        sdk.update_dashboard(dash_id, body=dashboardobject)
        export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.source_folder)
