import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    try:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except:
        return (f"Error: Issue with commonpath")
        
    valid_directory = os.path.isdir(target_dir)


    if not valid_target_dir:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not valid_directory:
        return (f'Error: "{directory}" is not a directory')
    result = "Result for current directory:"

    items = []
    try:
        contents = os.listdir(target_dir)
    except:
        return (f"Error: Issue with listdir")

    for item in contents:
        path = os.path.join(target_dir, item)
        try:
            items.append(f" - {item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")
        except:
            return (f"Error: Issue with path")
    
    for item in items:
        result = result + "\n" + item
    return result

