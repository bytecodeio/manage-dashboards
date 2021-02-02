from utils import export_content
from utils import git_repo
import json


def export(args, catalog_file, folder_id, dash_id, repo, folder):
    export_content.export(args, folder_id)
    commit_message = f"Dash {args.name}, id {dash_id} updated in {folder}"
    sha = git_repo.write_to_repo(repo, commit_message)
    with open(catalog_file, 'r+') as catfile:
        catalog = json.load(catfile)
    if folder not in catalog.keys():
        catalog[folder] = []
    dash_index = next((i for i, dash in enumerate(catalog[folder]) if dash['id'] == dash_id), None)
    if dash_index is None:
        catalog[folder].append({
            'id': dash_id,
            'version': args.version,
            'name': args.name,
            'commit': sha
        })
    else:
        previous_version = catalog[folder][dash_index]['version']
        previous_commit = catalog[folder][dash_index]['commit']
        catalog[folder][dash_index] = {
            'id': dash_id,
            'version': args.version,
            'name': args.name,
            'commit': sha
        }
        catalog[folder][dash_index]['previous'] = {
                'version': previous_version,
                'commit': previous_commit
        }
    with open(catalog_file, 'w') as catfile:
        json.dump(catalog, catfile, indent=4, sort_keys=True)
    git_repo.write_to_repo(repo, 'Updated catalog file')
