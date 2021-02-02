import json
from utils.get_client import get_client
from utils import export_dash, find_file, git_repo, import_dash, parse_ini
import os


def main(args, catalog_file, repo):
    sdk = get_client(args.ini, args.env)
    folder_results = sdk.search_folders(name=args.source_folder)
    ini = parse_ini.read_ini(args.ini)
    config = ini[args.env]
    local_git_dir = config["local_git_dir"]

    if len(folder_results) == 0:
        print("{} folder does not exist".format(args.source_folder))
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
            print(f"Source folder {args.source_folder} not found in catalog")
            exit(1)

        dash_index = next((i for i, dash in enumerate(catalog[args.source_folder]) if dash['id'] == dash_id), None)
        if dash_index is None:
            print(f"{args.name} in folder {args.source_folder} does not exist in catalog file")
            exit(1)

        if args.archive:
            print("Exporting dashboard before archiving")
            export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.source_folder)
            filename = find_file.get_filename(local_git_dir, dash_id, args.source_folder)
            import_dash.import_dash(filename, args, args.archive_folder)

            folder_results_a = sdk.search_folders(name=args.archive_folder)
            folder_id_a = folder_results_a[0].id
            results = sdk.search_dashboards(title=args.name, folder_id=folder_id_a)
            dash_id_a = results[0].id
            export_dash.export(args, catalog_file, folder_id_a, dash_id_a, repo, args.archive_folder)

        sdk.delete_dashboard(dash_id)
        with open(catalog_file, 'r+') as catfile:
            catalog = json.load(catfile)
        del catalog[args.source_folder][dash_index]
        with open(catalog_file, 'w') as catfile:
            json.dump(catalog, catfile)
        git_repo.write_to_repo(repo, 'Updated catalog file')

        filename = find_file.get_filename(local_git_dir, dash_id, args.source_folder)

        try:
            os.remove(filename)
            git_repo.write_to_repo(repo, f"Removed dashboard {args.name} from folder {args.source_folder}")
        except OSError as err:
            print(f"Error: {local_git_dir} : {err}")
