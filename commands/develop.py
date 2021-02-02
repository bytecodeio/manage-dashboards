import json
from utils.get_client import get_client
from utils import export_dash, find_file, import_dash, parse_ini


def main(args, catalog_file, repo):
    sdk = get_client(args.ini, args.env)
    folder_results = sdk.search_folders(name=args.source_folder)
    ini = parse_ini.read_ini(args.ini)
    config = ini[args.env]

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
            catalog[args.source_folder] = []
        dash_index = next((i for i, dash in enumerate(catalog[args.source_folder]) if dash['id'] == dash_id), None)
        if dash_index is None:
            print(f"{args.name} does not exist in catalog file, exporting to git before importing to {args.target_folder}")
            export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.source_folder)
        filename = find_file.get_filename(config['local_git_dir'], dash_id, args.source_folder)
        import_dash.import_dash(filename, args, args.target_folder)
        print(f"Imported dashboard {args.name} to {args.target_folder} from {filename}")
        folder_results = sdk.search_folders(name=args.target_folder)
        folder_id = folder_results[0].id
        results = sdk.search_dashboards(title=args.name, folder_id=folder_id)
        dash_id = results[0].id
        export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.target_folder)
        print(f"Dashboard {args.name} from {args.target_folder} exported to git")
