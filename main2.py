import shutil
import os

def backup_exported_photos(photo_folder, backup_location):
    for root, dirs, files in os.walk(photo_folder):
        for dir in dirs:
            if dir == "Export":
                export_folder = os.path.join(root, dir)
                parent_folder_name = os.path.basename(os.path.dirname(export_folder))
                backup_folder = os.path.join(backup_location, parent_folder_name)

                if not os.path.exists(backup_folder):
                    os.makedirs(backup_folder)

                for filename in os.listdir(export_folder):
                    if filename.endswith(".jpg"):
                        source_file = os.path.join(export_folder, filename)
                        destination_file = os.path.join(backup_folder, filename)

                        shutil.copy(source_file, destination_file)

if __name__ == "__main__":
    photo_folder = "D:/BTest"
    backup_location = "E:/After"

    backup_exported_photos(photo_folder, backup_location)