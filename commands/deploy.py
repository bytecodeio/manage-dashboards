import json
from utils.get_client import get_client
from utils import export_dash, find_file, import_dash
from utils import git_repo
import shutil


def main(args, catalog_file, repo):
    sdk = get_client(args.ini, args.env)
    with open(catalog_file, 'r+') as catfile:
        catalog = json.load(catfile)
    dash_index = next((i for i, dash in enumerate(catalog[args.source_folder]) if dash['name'] == args.name), None)
    if dash_index is None:
        print(f"Catalog entry for {args.name} not found for folder {args.source_folder}")
        exit(1)
    else:
        commit = catalog[args.source_folder][dash_index]['commit']
        dash_id = catalog[args.source_folder][dash_index]['id']
        cat_version = catalog[args.source_folder][dash_index]['version']

    if args.version != cat_version:
        print(f"Version in catalog {cat_version}, does not match parameter version {args.version}.  Do you need to update first?")
        exit(1)
    temp_git_folder = './temp_git/'
    git_repo.checkout_commit(args.ini, args.env, commit, temp_git_folder)
    filename = find_file.get_filename(temp_git_folder, dash_id, args.source_folder)
    import_dash.import_dash(filename, args, args.target_folder)
    print(f"Dashboard {args.name} imported to {args.target_folder}")

    folder_results = sdk.search_folders(name=args.target_folder)
    folder_id = folder_results[0].id
    results = sdk.search_dashboards(title=args.name, folder_id=folder_id)
    dash_id = results[0].id
    export_dash.export(args, catalog_file, folder_id, dash_id, repo, args.target_folder)
    print(f"Dashboard {args.name} from {args.target_folder} exported to git")
    try:
        shutil.rmtree(temp_git_folder)
    except OSError as err:
        print(f"Error: {temp_git_folder} : {err}")
