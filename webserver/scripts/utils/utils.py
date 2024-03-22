import os


def delete_files_in_directory(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {directory} deleted.")
    except Exception as e:
        print(f"Error deleting files: {str(e)}")
