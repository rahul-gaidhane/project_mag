import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library 

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
    try:
        f = open('index.html', 'w')
    except FileExistsError:
        pass
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

def GenJpegImages(TiffDirPath, JpegDirPath):
    print("Inside GenJpegImages:\n")
    print("TiffDirPath = %s\n" % (TiffDirPath))
    print("JpegDirPath = %s\n" % (JpegDirPath))
    JpegDirPath = JpegDirPath + '/JPEG_FILES'
    try:
        os.mkdir(JpegDirPath)
    except FileExistsError:
        pass
    TiffFileList = os.listdir(TiffDirPath)
    os.chdir(JpegDirPath)
    for TiffFile in TiffFileList:
        TiffFilename = TiffFile.split('.')[0]
        TiffFilePath = TiffDirPath + '/' + TiffFile
        if GetFileType(TiffFilePath) == 'tiff':
            try:
                os.mkdir(TiffFilename)
            except FileExistsError:
                pass
            os.chdir(TiffFilename)
            img = Image.open(TiffFilePath)
            for imgcount in range(1000):
                try:
                    img.seek(imgcount)
                    img.save('%s-%d.jpeg' % (TiffFilename, imgcount))
                except EOFError:
                    break
            os.chdir('..')
        else:
            print('Module yet to be generated')


def GenThumbnailImages(TiffDirPath, ThumbnailDirPath):
    print("Inside GenThumbnailImages:\n")
    print("TiffDirPath = %s\n" % (TiffDirPath))
    print("ThumbnailDirPath = %s\n" % (ThumbnailDirPath))

def GenHtmlFiles(OutputDirPath):
    print("Inside GenHtmlFiles:\n")
    print("OutputDirPath = %s\n" % (OutputDirPath))

def GetFileType(FilePath):
    print('Inside GetFileType = %s' % (FilePath))
    return (magic.from_file(FilePath, mime=True)).split('/')[1]
