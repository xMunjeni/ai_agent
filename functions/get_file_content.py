import os
from config import MAX_CHAR_LEN

def get_file_content(working_directory, file_path):

    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    except:
        return (f"Error: Issue with commonpath")
        
    valid_path = os.path.isfile(target_file)


    if not valid_target_file:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not valid_path:
        return (f'Error: File not found or is not a regular file: "{file_path}"')

    
    try:
        file = open(target_file)
    except:
        return (f'Error: Cannot open "{file_path}"')
    
    try:
        content = file.read(MAX_CHAR_LEN)
    except:
        return (f'Error: Cannot read file at "{file_path}"')

    if file.read(1):
        content += f'[...File "{file_path}" truncated at {MAX_CHAR_LEN} characters]'
    
    close(file_path)
    return content
    





    
    