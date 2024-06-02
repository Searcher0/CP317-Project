import os

def create_folders_and_files(base_path, list_file_path):
    # Read the list of folder names from the file
    with open(list_file_path, 'r') as file:
        folder_names = [line.strip() for line in file]

    # Create folders and files
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

# Define the base path and the path to the file containing folder names
base_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FILES\Fruits & Vegetables'
list_file_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\Fruits&Veg.txt'  # Update this to the path of your list file

# Call the function to create folders and files
create_folders_and_files(base_path, list_file_path)
