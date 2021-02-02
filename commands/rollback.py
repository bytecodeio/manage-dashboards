import json
from utils.get_client import get_client
from utils import git_repo, find_file, import_dash
import shutil


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
        dash_index = next((i for i, dash in enumerate(catalog[args.source_folder]) if dash['id'] == dash_id), None)
        if dash_index is None:
            print(f"Dashboard {args.name} not found in catalog file for folder {args.source_folder}?")
            exit(1)
        elif "previous" not in catalog[args.source_folder][dash_index].keys():
            print(f"Dashboard {args.name} in folder {args.source_folder}, previous version not found")
            exit(1)
        else:
            commit = catalog[args.source_folder][dash_index]['previous']['commit']
            dash_id = catalog[args.source_folder][dash_index]['id']
            temp_git_folder = './temp_git/'
            git_repo.checkout_commit(args.ini, args.env, commit, temp_git_folder)
            filename = find_file.get_filename(temp_git_folder, dash_id, args.source_folder)
            import_dash.import_dash(filename, args, args.source_folder)
            version = catalog[args.source_folder][dash_index]['previous']['version']
            commit = catalog[args.source_folder][dash_index]['previous']['commit']
            previous_version = catalog[args.source_folder][dash_index]['version']
            previous_commit = catalog[args.source_folder][dash_index]['commit']
            catalog[args.source_folder][dash_index] = {
                'id': dash_id,
                'version': version,
                'name': args.name,
                'commit': commit
            }
            catalog[args.source_folder][dash_index]['previous'] = {
                'version': previous_version,
                'commit': previous_commit
            }
            with open(catalog_file, 'w') as catfile:
                json.dump(catalog, catfile, indent=4, sort_keys=True)
            git_repo.write_to_repo(repo, 'Updated catalog file')
            try:
                shutil.rmtree(temp_git_folder)
            except OSError as err:
                print(f"Error: {temp_git_folder} : {err}")
