import os
import shutil
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
        writer.writerow(['Folder original path', 'Final path', 'Name', 'File Type', 'Date created', 'Size (B)', 'Date last accessed', 'Accessed in the last month?'])

        for path in paths:

            newDocDirectory = "Docs"
            # Docs -> docx, doc, xlsx
            # Pdfs -> pdf
            # Images -> png, jpg, jpeg
            # Videos -> mp4, mov
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
                        filePathWoExt, fileExtension = os.path.splitext(filePath)

                        if (datetime.now() - lastAccessed < timedelta(days = 30)):
                            flag = 'Yes'
                        else:
                            flag = 'No'
                        
                        destDirPath = ''

                        fileExtension = fileExtension.lower()

                        if fileExtension in ('.docx', '.doc', '.xlsx', '.xls'):
                            destDirPath = os.path.join(path, "Docs")
                            shutil.move(filePath, os.path.join(destDirPath, name))
                        elif fileExtension == ('.pdf'):
                            destDirPath = os.path.join(path, "Pdfs")
                            shutil.move(filePath, os.path.join(destDirPath, name))
                        elif fileExtension in ('.png', '.jpg', '.jpeg'):
                            destDirPath = os.path.join(path, "Images")
                            shutil.move(filePath, os.path.join(destDirPath, name))
                        elif fileExtension in ('.mp4', '.mov'):
                            destDirPath = os.path.join(path, "Videos")
                            shutil.move(filePath, os.path.join(destDirPath, name))
                        elif fileExtension in ('.mp3', '.wav'):
                            destDirPath = os.path.join(path, "Audio")
                            shutil.move(filePath, os.path.join(destDirPath, name))
                        else:
                            destDirPath = os.path.join(path, "Misc")
                            shutil.move(filePath, os.path.join(destDirPath, name))

                        writer.writerow([path, destDirPath, name, fileExtension, dateCreated, size, lastAccessed, flag])

if __name__ == "__main__":
    main()
