import argparse
import hashlib
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

moved_file_count = 0


def upload_files_to_google_drive(service, backup_dir):
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            if file.endswith(".jpg"):
                source_file = os.path.join(root, file)
                destination_file = file
                print(file)

                if not file_exists_in_google_drive(service, destination_file) or needs_update(source_file, destination_file):
                    upload_file_to_google_drive(service, source_file, destination_file)
                    moved_file_count += 1
                    print(moved_file_count)


def file_exists_in_google_drive(service, file_name):
    try:
        service.files().get(fileId=file_name).execute()
        return True
    except:
        return False

def upload_file_to_google_drive(service, source_file, destination_file):
    with open(source_file, "rb") as f:
        metadata = {'name': destination_file}
        media_body = MediaFileUpload(f, chunksize=-1, resumable=True)
        service.files().create(body=metadata, media_body=media_body).execute()

def needs_update(source_file, destination_file):
    source_hash = generate_md5_hash(source_file)
    destination_hash = generate_md5_hash(destination_file) if file_exists_in_google_drive(service, destination_file) else None

    return source_hash != destination_hash

def generate_md5_hash(filename):
    with open(filename, "rb") as f:
        hasher = hashlib.md5()

        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)

        return hasher.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup exported photos from a photo folder directly to Google Drive")
    parser.add_argument("--photodir", type=str, required=True, help="Path to the photo folder")

    args = parser.parse_args()

    photodir = args.photodir

    service = build('drive', 'v3')

    upload_files_to_google_drive(service, photodir)

    print("Total uploaded files:", moved_file_count)