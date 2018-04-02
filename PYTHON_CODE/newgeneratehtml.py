import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library
import subprocess

def main(InputDir, OutputDir):
    if OutputDir == "":
        OutputDir = os.getcwd() + '/Output'
    else:
        OutputDir = OutputDir + '/Output'
    try:
        os.mkdir(OutputDir)
    except FileExistsError:
        pass
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
        InputAnnualDirPath = InputDir + '/' + InputAnnualDir
        OutputAnnualDirPath = OutputDir + '/' + InputAnnualDir
        try:
            os.mkdir(OutputAnnualDirPath)
        except FileExistsError:
            pass
        GenJpegImages(InputAnnualDirPath, OutputAnnualDirPath)
        GenThumbnailImages(InputAnnualDirPath, OutputAnnualDirPath)
        GenHtmlFiles(OutputAnnualDirPath)
        GenMetaFiles(OutputAnnualDirPath)
        f.write('\t\t<p><a href="%s/AnnualList.html">%s</a></p>\n' % (InputAnnualDir, InputAnnualDir))
    f.write('\t<body>\n')
    f.write('</html>\n')
    f.close()

def GenMetaFiles(OutputDirPath):
    print("Inside GenMetaFiles:\n")
    print("OutputDirPath = %s" % (OutputDirPath))

def GenJpegImages(ArchiveDirPath, JpegDirPath):
    print("Inside GenJpegImages:\n")
    print("ArchiveDirPath = %s\n" % (ArchiveDirPath))
    print("JpegDirPath = %s\n" % (JpegDirPath))
    JpegDirPath = JpegDirPath + '/JPEG_FILES'
    try:
        os.mkdir(JpegDirPath)
    except FileExistsError:
        pass
    ArchiveFileList = os.listdir(ArchiveDirPath)
    os.chdir(JpegDirPath)
    for ArchiveFile in ArchiveFileList:
        ArchiveFileName = ArchiveFile.split('.')[0]
        ArchiveFilePath = ArchiveDirPath + '/' + ArchiveFile
        JpegArchivePath = JpegDirPath + '/' + ArchiveFileName
        try:
            os.mkdir(ArchiveFileName)
        except FileExistsError:
            pass
        os.chdir(ArchiveFileName)
        if GetFileType(ArchiveFilePath) == 'tiff':
            img = Image.open(ArchiveFilePath)
            for imgcount in range(1000):
                try:
                    img.seek(imgcount)
                    img.save('%s-%d.jpeg' % (ArchiveFileName, imgcount))
                except EOFError:
                    break
            os.chdir('..')
        elif GetFileType(ArchiveFilePath) == 'pdf':
            JpegArchiveFile = JpegArchivePath + '/' + ArchiveFileName + '.jpeg'
            print('Inside pdf conversion\nJpegArchiveFile = %s\nArchiveFilePath = %s' % (JpegArchiveFile, ArchiveFilePath))
            f = open('/dev/null', 'w')
            subprocess.call(['convert', '-trim', '-density', '200', ArchiveFilePath, '-quality', '100', JpegArchiveFile], stderr=f)
    #        os.system('convert -trim -density 200 %s -quality 100 %s 2>/dev/null' % (ArchiveFilePath, JpegArchiveFile))
            os.chdir('..')
        else:
            print("FileTypeError : In apropriate File detected\nFilePath = %s" % (ArchiveFilePath))

def GenThumbnailImages(FileDirPath, ThumbnailDirPath):
#    print("Inside GenThumbnailImages:\n")
#    print("FileDirPath = %s\n" % (FileDirPath))
#    print("ThumbnailDirPath = %s\n" % (ThumbnailDirPath))


def GenHtmlFiles(OutputDirPath):
    print("Inside GenHtmlFiles:\n")
    print("OutputDirPath = %s\n" % (OutputDirPath))

def GetFileType(FilePath):
    return (magic.from_file(FilePath, mime=True)).split('/')[1]
