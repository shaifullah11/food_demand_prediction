import os

def rename_files(directory):
    for filename in os.listdir(directory):
        if ' ' in filename:
            new_filename = filename.replace(' ', '-')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed '{filename}' to '{new_filename}'")

# Replace 'path_to_your_directory' with the path to your image folder
directory = 'C:/Users\\shaif\\Desktop\\supplychain\\supplychain\\media\\uploads\\ingredient'
rename_files(directory)
