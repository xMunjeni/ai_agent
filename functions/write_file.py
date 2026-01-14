import os

def write_file(working_directory, file_path, content):
    
    #Define working directory and target file
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    #check for file path issues
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    except ValueError:
        return (f"Error: Issue with commonpath")
        
      

    #check if file is in permitted directory
    if not valid_target_file:
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    #if file path points to directory, error
    if os.path.isdir(target_file):
        return(f'Error: Cannot write to "{file_path}" as it is a directory')

    
    #check if parent directories exist:
    parent_dir = os.path.dirname(target_file)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    try:
        with open(target_file, "w") as f:
            f.write(content)
    except OSError:
        return (f'Error: Cannot write to "{file_path}"')
        
    return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')


