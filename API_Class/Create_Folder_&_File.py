import os

def create_folders_and_files(base_path, list_file_path):
    with open(list_file_path, 'r') as file:
        folder_names = [line.strip() for line in file]

    for folder_name in folder_names:
        # Strip leading and trailing spaces from folder names
        folder_name = folder_name.strip()
        
        # Create the folder
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create the file within the folder
        file_name = f'HTML_{folder_name}.txt'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write('')  # Create an empty file

base_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FILES\Snacks, Chips & Candy'
list_file_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\Text Files\Snacks, Chips & Candy.txt'

create_folders_and_files(base_path, list_file_path)
