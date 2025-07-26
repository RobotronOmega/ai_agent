import os

def get_files_info(working_directory, directory="."):
    directory = os.path.join(working_directory, directory)
    if not directory.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    result = ""
    dir_list = os.listdir(directory)
    for item in dir_list:
        item_path = os.path.join(directory, item)
        result += " - " + item + ": file size=" + str(os.path.getsize(item_path)) + " bytes, is_dir=" + str(os.path.isdir(item_path)) + "\n"

    return result