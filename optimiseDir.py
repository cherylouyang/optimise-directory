import os
import csv
from datetime import datetime, timedelta

def main():
    print("Folder path/s:")
    paths = []
    while True:
        path = input()
        if path:
            paths.append(path)
        else:
            break

    with open('optimiseResults.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Folder path', 'Name', 'File Type', 'Date created', 'Size (B)', 'Date last accessed', 'Accessed in the last month?'])

        for path in paths:

            newDocDirectory = "Docs"
            # Docs -> docx, doc, xlsx
            # Pdfs -> pdf
            # Images -> png, jpg, jpeg
            # Videos -> mp4
            # Audio -> mp3, wav
            newDirectories = ["Docs", "Pdfs", "Images", "Videos", "Audio", "Misc"]
            for dir in newDirectories:
                newDirPath = os.path.join(path, dir)

                # create folders for sorting file types
                if not os.path.exists(newDirPath):
                    os.makedirs(newDirPath)

            with os.scandir(path) as dirEntries:
                for entry in dirEntries:
                    if entry.is_file():
                        info = entry.stat()
                        name = entry.name
                        size = info.st_size
                        dateCreated = datetime.fromtimestamp(info.st_ctime)
                        # lastModified = datetime.fromtimestamp(info.st_mtime)
                        lastAccessed = datetime.fromtimestamp(info.st_atime)

                        filePath = os.path.join(path, name)
                        fileName, fileExtension = os.path.splitext(filePath)

                        if (datetime.now() - lastAccessed < timedelta(days = 30)):
                            flag = 'Yes'
                        else:
                            flag = 'No'

                        writer.writerow([path, name, fileExtension, dateCreated, size, lastAccessed, flag])

if __name__ == "__main__":
    main()
