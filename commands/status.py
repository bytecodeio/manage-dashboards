import json

def main(args, catalog_file, repo):
    with open(catalog_file, 'r+') as catfile:
        catalog = json.load(catfile)
    print(json.dumps(catalog, indent=4, sort_keys=True))
