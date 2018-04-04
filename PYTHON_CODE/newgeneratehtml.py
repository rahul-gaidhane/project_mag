import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library
import subprocess

def MakeDir(DirPath):
    try:
        os.mkdir(DirPath)
    except FileExistsError:
        pass

def main(InputDir, OutputDir):
    if OutputDir == "":
        OutputDir = os.path.join(os.getcwd(), 'Output')
    else:
        OutputDir = os.path.join(OutputDir, 'Output')
    MakeDir(OutputDir)
    InputAnnualDirList = os.listdir(InputDir)
    os.chdir(OutputDir)
    f = open('index.html', 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>Aajcha Sudharak</title>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<h1>List Of Annual Issues</h1>\n')
    for InputAnnualDir in InputAnnualDirList:
        InputAnnualDirPath = os.path.join(InputDir, InputAnnualDir)
        OutputAnnualDirPath = os.path.join(OutputDir, InputAnnualDir)
        MakeDir(OutputAnnualDirPath)
        GenJpegThumbImages(InputAnnualDirPath, OutputAnnualDirPath)
        GenHtmlFiles(OutputAnnualDirPath)
        #GenMetaFiles(OutputAnnualDirPath)
        f.write('\t\t<p><a href="%s/AnnualList.html">%s</a></p>\n' % (InputAnnualDir, InputAnnualDir))
    f.write('\t<body>\n')
    f.write('</html>\n')
    f.close()

def GenMetaFiles(OutputDirPath):
    print("Inside GenMetaFiles:\n")
    print("OutputDirPath = %s" % (OutputDirPath))

def GenJpegThumbImages(ArchiveDirPath, OutputDirPath):
    print("Inside GenJpegThumbImages:\n")
    print("ArchiveDirPath = %s\n" % (ArchiveDirPath))
    print("OutputDirPath = %s\n" % (OutputDirPath))
    JpegDirPath = os.path.join(OutputDirPath, 'JPEG_FILES')
    ThumbnailDirPath = os.path.join(OutputDirPath, 'THUMBNAIL_FILES')
    MakeDir(JpegDirPath)
    MakeDir(ThumbnailDirPath)
    ArchiveDirFileList = os.listdir(ArchiveDirPath)
    for ArchiveFile in ArchiveDirFileList:
        ArchiveFileName = ArchiveFile.split('.')[0]
        ArchiveFilePath = os.path.join(ArchiveDirPath, ArchiveFile)
        JpegMonthDirPath = os.path.join(JpegDirPath, ArchiveFileName)
        ThumbnailMonthDirPath = os.path.join(ThumbnailDirPath, ArchiveFileName)
        MakeDir(JpegMonthDirPath)
        MakeDir(ThumbnailMonthDirPath)
        if os.path.splitext(ArchiveFilePath)[1] == '.tif':
            img = Image.open(ArchiveFilePath)
            for imgcount in range(1000):
                try:
                    img.seek(imgcount)
                except EOFError:
                    break
                ImageFile = '%s-%d.jpeg' % (ArchiveFileName, imgcount)
                JpegImagePath = os.path.join(JpegMonthDirPath, ImageFile)
                img.save(JpegImagePath)
                newimg = Image.open(JpegImagePath)
                ThumbnailImagePath = os.path.join(ThumbnailMonthDirPath, ImageFile)
                newimg.thumbnail((300,500))
                newimg.save(ThumbnailImagePath)
        elif os.path.splitext(ArchiveFilePath)[1] == '.pdf':
            ImageFile = '%s.jpeg' % (ArchiveFileName)
            JpegImagePath = os.path.join(JpegMonthDirPath, ImageFile)
            ThumbnailImagePath = os.path.join(ThumbnailMonthDirPath, ImageFile)
            f = open('/dev/null', 'w')
            subprocess.call(['convert', '-trim', '-density', '200', ArchiveFilePath, '-quality', '100', JpegImagePath ], stderr=f)
            subprocess.call(['convert', '-trim', ArchiveFilePath, '-resize', '300', '-quality', '100', ThumbnailImagePath ], stderr=f)
        else:
            print("FileTypeError : In apropriate File detected\nFilePath = %s" % (ArchiveFilePath))

def GenHtmlFiles(OutputDirPath):
    print("Inside GenHtmlFiles:\n")
    print("OutputDirPath = %s\n" % (OutputDirPath))

def Makedir(DirPath):
    try:
        os.mkdir(DirPath)
    except FileExistsError:
        pass
