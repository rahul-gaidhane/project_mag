def imports():
    print("Inside imports()\n")
    import os
import os

def main(InputDir, OutputDir):
    if OutputDir == "":
        OutputDir = os.getcwd() + '/Output'
    else:
        OutputDir = OutputDir + '/Output'
    os.mkdir(OutputDir)
    InputAnnualDirList = os.listdir(InputDir)
    CurrentDirPath = os.getcwd()
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
        os.mkdir(OutputAnnualDirPath)
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

def GenThumbnailImages(TiffDirPath, ThumbnailDirPath):
    print("Inside GenThumbnailImages:\n")
    print("TiffDirPath = %s\n" % (TiffDirPath))
    print("ThumbnailDirPath = %s\n" % (ThumbnailDirPath))

def GenHtmlFiles(OutputDirPath):
    print("Inside GenHtmlFiles:\n")
    print("OutputDirPath = %s\n" % (OutputDirPath))
