def read_file(file_path: str):

    with open(file_path, mode='r', encoding='utf-8') as file:
        file_bytes = file.read().encode('utf-8')
    
    return file_bytes