import os


def get_filename(local_folder, dash_id, folder):
    id_line = '"dashboard_id": {},'.format(dash_id)
    search_path = local_folder + "Shared/" + folder + "/"
    for filename in os.listdir(search_path):
        with open(search_path + filename, 'r') as file:
            for line in file:
                index = line.find(id_line)
                if index != -1:
                    return search_path + filename
    print(f"Unable to locate file for the specified dashboard id {dash_id} in folder {folder}")
    exit(1)
