import os
from arctrl.arc import ARC
from utils.Contracts import fulfill_read_contract


def normalize_path_separators(path_str: str):
    normalized_path = os.path.normpath(path_str)
    return normalized_path.replace('//', '/')


def get_all_file_paths(base_path):
    files_list = []

    def loop(dir_path):
        files = os.listdir(dir_path)
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                loop(file_path)
            else:
                relative_path = os.path.relpath(file_path, base_path)
                normalize_path = normalize_path_separators(relative_path)
                files_list.append(normalize_path)
    loop(base_path)
    return files_list


def read(base_path):
    all_file_paths = get_all_file_paths(base_path)
    arc = ARC.from_file_paths(all_file_paths)
    read_contracts = arc.GetReadContracts()
    _ = [fulfill_read_contract(base_path, contract)
         for contract in read_contracts]
    arc.SetISAFromContracts(read_contracts)
    return arc
