Hi! 

This is a program to backup .jpg's from a photography file tree, keeping their folder / file names in order to upload them / back them up.

This program is a photo backup solution I made for my photography workflow, as I have a really odd and specific way of handling my library. It essentially looks for .jpg files, inside an export folder. It looks like this:

Source Directory:
```
Photos/
├── Jerry/
│ └── Export/
│ ├── Upload/
│ │ ├── Photo1.jpg
│ │ ├── Photo2.jpg
│ ├── Photo3.jpg
│ └── Photo4.jpg
├── Liam/
│ └── Export/
│ ├── Image1.jpg
│ ├── Image2.jpg
│ └── Image3.jpg
├── Riley/
│ └── Export/
│ └── Pic1.jpg
```
Destination Directory:
```
Destination/
├── Jerry/
│ ├── Photo1.jpg
│ ├── Photo2.jpg
├── Liam/
│ ├── Image1.jpg
│ ├── Image2.jpg
│ └── Image3.jpg
├── Riley/
│ └── Pic1.jpg
```
So if an upload folder exists within export, it will only take those, otherwise it will take all images from export. 

If your photo directory doesnt look like this, it shouldn't work, but feel free to change it to whatever you need!
```
USAGE:
python3 PhotoBackup.py ----sourceDir "source/folder/directory" --destDir "/destination/of/backup/or/upload"
```

This can then be piped for Google Drive Uploading, and can be run on a chron schedule. 
