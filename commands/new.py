from utils.get_client import get_client
from utils import export_dash
import looker_sdk


def main(args, catalog_file, repo):
    sdk = get_client(args.ini, args.env)

    folder_results = sdk.search_folders(name=args.target_folder)
    folder_id = folder_results[0].id
    results = sdk.search_dashboards(title=args.name, folder_id=folder_id)

    if len(results) == 1:
        print("Target dashboard exists, did you mean to update?")
        exit(0)
    elif len(results) == 0:
        print(f"Dashboard {args.name} not found in folder {args.target_folder}, creating")
        dashboardobject = looker_sdk.models.WriteDashboard(
            title=args.name,
            space_id=folder_id
        )
        results = sdk.create_dashboard(body=dashboardobject)
        export_dash.export(args, catalog_file, folder_id, results.id, repo, args.target_folder)
