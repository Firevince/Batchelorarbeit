import glob
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


def delete_oldest_files(directory_path, threshold=50, amount=10):
    files = glob.glob(os.path.join(directory_path, "*"))
    if len(files) > threshold:
        # Sort the files by modification time, oldest first
        files.sort(key=os.path.getmtime)
        for file in files[:amount]:
            os.remove(file)
            print(f"Deleted {file}")


def create_data_folders():
    os.makedirs("/app/data/Podcast_Episoden", exist_ok=True)
    os.makedirs("/app/data/audio_segments", exist_ok=True)
