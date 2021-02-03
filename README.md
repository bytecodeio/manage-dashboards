# Manage Dashboards

This is a custom python script that wraps Looker Deployer to provide version tracking for Looker dashboards and to facilitate moving content between folders on the same Looker instance.
In order to facilitate this, a json catalog file is created to track the versions(user specified) of dashboards and the corresponding commits in git.

It is important to note that once you start using this tool to manage a dashboard, any renames, deletes or copies should be done with this tool.  If not, the catalog file will be out of sync or you can be left with orphaned content files in the repo, diminishing the usefulness of this tool.

The tool also uses the "Shared" folder in Looker as the base folder for all operations

## Requirements
>- **Python** Requires Python 3.6+
>- **Looker Deployer** https://pypi.org/project/looker-deployer/
>- **Gazer** https://github.com/looker-open-source/gzr
>- **Git Repo** For storing the exported content and the catalog file

## Authentication
This script and Looker Deployer use the `looker.ini` file for authentication information.  By default the script looks for the file in the working directory but the name or location can be specified with the `ini` argument.
```
[dev]
base_url=https://looker-dev.company.com:19999
client_id=abc
client_secret=xyz
verify_ssl=True
git_token=abc123
git_base=github.com/org/repo
git_user=githubusername
git_email=name@company.com
local_git_dir=./git_repo/
catalog_file=./git_repo/dash_catalog.json

[prod]
base_url=https://looker-prod.company.com:19999
client_id=abc
client_secret=xyz
verify_ssl=True
git_token=abc123
git_base=github.com/org/repo
git_user=githubusername
git_email=name@company.com
local_git_dir=./git_repo/
catalog_file=./git_repo/dash_catalog.json
```
## Installation
To begin, clone this repo to your local machine.

Install gazer `gem install gazer`

Install python packages (includes looker_deployer) `pip install -r requirements.txt`

## Usage
The script can be run with various sub-commands.  Available sub-commands are: `delete`, `deploy`, `develop`, `new`, `rename`, `rollback`, `status`, and `update`.

In the examples given below, all commands must start with:`python manage_dashboards.py `

### Delete
Delete the specified dashboard from the source folder, with the option to archive it first
```
usage: manage_dashboard.py delete [-h] --name NAME [--ini INI] --env ENV
                      [--source_folder SOURCE_FOLDER]
                      [--archive_folder ARCHIVE_FOLDER] [--archive ARCHIVE]
                      [--version VERSION]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to delete
  --ini INI             ini file to parse for credentials
  --env ENV             What environment to interact with
  --source_folder SOURCE_FOLDER
                        folder to delete dashboard in
  --archive_folder ARCHIVE_FOLDER
                        folder to archive dashboard in
  --archive ARCHIVE     should dashboard be archived
  --version VERSION     dashboard version if archiving
```
### Examples:

`delete --name "dash3" --env dev --source_folder Development --archive True --version 1.0` -- deletes the dashboard "dash3" from the Looker `Shared/Development` folder and imports it to the `Shared/Archive` folder. Removes the entry for `Development` and adds it as version 1.0 to `Archive` in the catalog file

`delete --name "dash3" --env dev --source_folder Development` -- deletes the dashboard "dash3" from the Looker `Shared/Development` folder and removes the entry from the catalog file

### Deploy
Deploy the specified dashboard and version from the source folder to the target folder
```
usage: manage_dashboard.py deploy [-h] --name NAME [--ini INI] --env ENV
                      [--target_folder TARGET_FOLDER]
                      [--source_folder SOURCE_FOLDER] --version VERSION

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to deploy
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --target_folder TARGET_FOLDER
                        folder to deploy to
  --source_folder SOURCE_FOLDER
                        folder to deploy from
  --version VERSION     new dashboard version
```

### Examples:

`deploy --name "dash2" --env dev --target_folder Staging --source_folder Development --version 1.1` -- reads the catalog file to get the commit for version `1.1` of the dashboard `dash2` in the `Shared/Development` folder, checks out that commit, imports `dash2` to `Shared/Staging`, and updates the catalog for `Staging`

### Develop
```
usage: manage_dashboard.py develop [-h] --name NAME [--ini INI] --env ENV
                       [--target_folder TARGET_FOLDER]
                       [--source_folder SOURCE_FOLDER] --version VERSION

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to develop
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --target_folder TARGET_FOLDER
                        folder to develop from
  --source_folder SOURCE_FOLDER
                        folder to develop in
  --version VERSION     new dashboard version
```

### Examples:

`develop --name "dash3" --env dev --target_folder Development --version 1.0` -- checks if the dashboard `dash3` in `Shared/Production`(default) is listed in the catalog, exports it and adds to catalog if not.  `dash3` is then imported to `Shared/Development` and updated in the catalog for `Development` as version `1.0`

### New

Create a new blank dashboard in the target folder
```
usage: manage_dashboard.py new [-h] --name NAME [--ini INI] --env ENV
                   [--target_folder TARGET_FOLDER] --version VERSION

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of new dashboard to create or update
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --target_folder TARGET_FOLDER
                        folder to create in
  --version VERSION     new dashboard version
```

### Examples:

`new --name "new dash" --env dev --target_folder Development --version 1.0` -- creates a blank dashboard `new dash` in `Shared/Development`, exports it and adds to the catalog for `Development` as version `1.0`

### Rename

If you are renaming a dashboard that is managed by this tool and it exists in multple folders, it is important to run this command on the dashboard in each folder.
```
usage: manage_dashboard.py rename [-h] --name NAME --new_name NEW_NAME [--ini INI] --env
                      ENV [--source_folder SOURCE_FOLDER] --version VERSION

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to rename
  --new_name NEW_NAME   new name for dashboard
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --source_folder SOURCE_FOLDER
                        folder in which to rename dashboard
  --version VERSION     new dashboard version
```

### Examples:

`rename --name "dash3" --env dev --new_name "dash4" --source_folder Development --version 1.2` -- renames the dashboard `dash3` in folder `Shared/Development` to `dash4`, exports the newly named dashboard, and adds to the catalog for `Development` as version `1.2`.  Removes old export files

### Rollback

The previous commit and version of each dashboard is saved in the catalog file.  Issuing the rollback command will import that dashboard at that commit to the specified folder.
Issuing a second rollback on the same dashboard will return it to the first version( eg. rollback from 1.1 -> 1.0, second rollback 1.0 -> 1.1)
```
usage: manage_dashboard.py rollback [-h] --name NAME [--ini INI] --env ENV
                        [--source_folder SOURCE_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to rollback
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --source_folder SOURCE_FOLDER
                        folder to rollback dashboard in
```

### Examples:

`rollback --name "dash3" --env dev --source_folder Production` -- looks up the previous version and commit for `dash3` in `Production`, checks out that commit and imports `dash3` to `Shared/Production`

### Status

Prints the catalog file
```
usage: manage_dashboard.py status [-h] [--ini INI] --env ENV

optional arguments:
  -h, --help  show this help message and exit
  --ini INI   ini file to parse for credentials
  --env ENV   what environment to interact with
```

### Examples:

`status --env dev`
```
{
    "Archive": [
        {
            "commit": "229a1cc6bc238339de7c895d85a60b2914e55571",
            "id": "65",
            "name": "dash3",
            "version": "1.0"
        }
    ],
    "Development": [
        {
            "commit": "02aa998c45ca3724723dd13abffe0af8b321970e",
            "id": "61",
            "name": "dash2",
            "version": "1.1"
        },
        {
            "commit": "e1335bb5236d774c42e149e00bfd34faaa89cc29",
            "id": "64",
            "name": "dash4",
            "previous": {
                "commit": "1982cadfe16885bf42de43180cabd3f524d49613",
                "version": "1.1"
            },
            "version": "1.2"
        }
    ]
}
```

### Update
Updates the catalog file and exports the dashboard
```
usage: manage_dashboard.py update [-h] --name NAME [--ini INI] --env ENV
                      [--source_folder SOURCE_FOLDER] --version VERSION

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           name of dashboard to update
  --ini INI             ini file to parse for credentials
  --env ENV             what environment to interact with
  --source_folder SOURCE_FOLDER
                        folder to update from
  --version VERSION     new dashboard version
```

### Examples:

`update --name "dash3" --env dev --source_folder Development --version 1.2` -- exports `dash3` in folder `Shared/Development` to git and updates the catalog entry to version `1.2`
