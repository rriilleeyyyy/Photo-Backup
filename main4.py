import argparse
import hashlib
import shutil
import os

moved_file_count = 0

def backup_exported_photos(photos, backup):
    global moved_file_count

    for root, dirs, files in os.walk(photos):
        if os.path.basename(root) == "Export":
            parent_folder_name = os.path.basename(os.path.dirname(root))
            backup_folder = os.path.join(backup, parent_folder_name)

            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            # Check if "Upload" subdirectory exists within "Export"
            upload_folder = os.path.join(root, "Upload")
            if os.path.exists(upload_folder):
                for file in os.listdir(upload_folder):
                    if file.endswith(".jpg"):
                        source_file = os.path.join(upload_folder, file)
                        destination_file = os.path.join(backup_folder, file)
                        if not os.path.exists(destination_file) or needs_update(source_file, destination_file):
                            shutil.copy2(source_file, destination_file)
                            moved_file_count += 1
                            print("Total moved or changed files:", moved_file_count, destination_file)

            # Copy other .jpg files from the Export folder (excluding "Upload" folder contents)
            for file in files:
                if file.endswith(".jpg") and not root.endswith("Upload"):
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join(backup_folder, file)
                    if not os.path.exists(destination_file) or needs_update(source_file, destination_file):
                        shutil.copy2(source_file, destination_file)
                        moved_file_count += 1
                        print("Total moved or changed files:", moved_file_count, destination_file)

def needs_update(source_file, destination_file):
    source_hash = generate_md5_hash(source_file)
    destination_hash = generate_md5_hash(destination_file) if os.path.exists(destination_file) else None
    return source_hash != destination_hash

def generate_md5_hash(filename):
    with open(filename, "rb") as f:
        hasher = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
        return hasher.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup exported photos from a photo folder to a backup location")
    parser.add_argument("--photodir", type=str, required=True, help="Path to the photo folder")
    parser.add_argument("--backupdir", type=str, required=True, help="Path to the backup location")

    args = parser.parse_args()

    photodir = args.photodir
    backupdir = args.backupdir

    backup_exported_photos(photodir, backupdir)

    print("Total moved or changed files:", moved_file_count)