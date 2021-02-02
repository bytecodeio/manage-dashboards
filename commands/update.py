import json
from utils.get_client import get_client
from utils import export_dash


def main(args, catalog_file, repo):
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
            print(f"{args.name} does not exist in catalog file, exporting to git and updating catalog")
            export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.source_folder)
        else:
            print(f"Updating catalog entry for {args.name} in folder {args.source_folder}")
            export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.source_folder)
