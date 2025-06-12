from os.path import abspath, join

def get_abs_paths(working_path, target_path):
    abs_working_path = abspath(working_path)
    abs_target_path = abs_working_path
    if target_path:
        abs_target_path = abspath(join(working_path, target_path))
    return abs_working_path, abs_target_path
