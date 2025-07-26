import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.join(working_directory, file_path)
        abs_work_directory = os.path.abs(working_directory)
        abs_file_path = os.path.abs(full_file_path)
        if not abs_file_path.startswith(abs_work_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # read file info into string, 1 more than MAX_CHARS
        with open(abs_file_path) as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) > MAX_CHARS:
            return file_content_string[:-1] + f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string

    except Exception as e:
        return f'Error: {e}'
    

        

    
