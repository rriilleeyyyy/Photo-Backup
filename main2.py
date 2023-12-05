import argparse
import hashlib
import shutil
import os

moved_file_count = 0

def backup_exported_photos(photos, backup):
    global moved_file_count

    for root, dirs, files in os.walk(photos):
        for dir in dirs:
            if dir == "Export":
                export_folder = os.path.join(root, dir)
                parent_folder_name = os.path.basename(os.path.dirname(export_folder))
                backup_folder = os.path.join(backup, parent_folder_name)

                if not os.path.exists(backup_folder):
                    os.makedirs(backup_folder)

                for filename in os.listdir(export_folder):
                    if filename.endswith(".jpg"):
                        source_file = os.path.join(export_folder, filename)
                        destination_file = os.path.join(backup_folder, filename)

                        if not os.path.exists(destination_file) or needs_update(source_file, destination_file):
                            shutil.copy(source_file, destination_file)
                            moved_file_count += 1

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