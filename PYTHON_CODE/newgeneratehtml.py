import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library
import subprocess


def main(InputDir, OutputDir):
    if OutputDir = "":
        OutputDir = os.path.join(os.getcwd(), 'Output')
    else:
        OutputDir = os.path.join(OutputDir, 'Output')
    MakeDir(OutputDir)
    InputAnnualDirList = os.listdir(InputDir)
    IndexHtmlPath = os.path.join(OutputDir, 'index.html')
    IndexFileObj = GetReadyIndexHtml(IndexHtmlPath)
    for InputAnnualDir in InputAnnualDirList:
        InputAnnualDirPath = os.path.join(InputDir, InputAnnualDir)
        OutputAnnualDirPath = os.path.join(OutputDir, InputAnnualDir)
        MakeDir(OutputAnnualDirPath)
        GenJpegThumbImages(InputAnnualDirPath, OutputAnnualDirPath)
        GenHtmlFiles(OutputAnnualDirPath)
        #GenMetaFiles(OutputAnnualDirPath)
        IndexFileObj = AddToIndexHtml(IndexFileObj, InputAnnualDir)
    CloseIndexHtml(IndexFileObj)

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
    HtmlDirPath = os.path.join(OutputDirPath, 'HTML_FILES')
    MakeDir(HtmlDirPath)
    JpegDirPath = os.path.join(OutputDirPath, 'JPEG_FILES')
    JpegMonthDirList = os.listdir(JpegDirPath)
    AnnualListHtmlPath = os.path.join(OutputDirPath, 'AnnualList.html')
    AnnualFileObj = GetReadyAnnualList(AnnualListHtmlPath)
    for JpegMonthDir in JpegMonthDirList:
        AnnualFileObj = AddToAnnualListHtml(AnnualFileObj, JpegMonthDir)
        HtmlMonthDirPath = os.path.join(HtmlDirPath, JpegMonthDir)
        MakeDir(HtmlMonthDirPath)
        JpegMonthDirPath = os.path.join(JpegDirPath, JpegMonthDir)
        JpegMonthImageList = os.listdir(JpegMonthDirPath)
        MaxPage = len(JpegMonthImageList)-1
        MonthListHtmlPath = os.path.join(HtmlDirPath, JpegMonthDir + '.html')
        MonthFileObj = GetReadyMonthList(MonthListHtmlPath)
        for ImageFile in JpegMonthImageList:
            ImageName = os.path.splitext(ImageFile)[0]
            MonthFileObj = AddToMonthListHtml(MonthFileObj, JpegMonthDir, ImageName)
            ImageHtmlPath = os.path.join(HtmlMonthDirPath, ImageName + '.html' )
            MakeImageHtml(ImageHtmlPath, JpegMonthDir, ImageName, MaxPage)
        CloseMonthList(MonthFileObj)
    CloseAnnualList(AnnualFileObj)

def GetReadyIndexHtml(IndexHtmlPath):
    IndexFileObj = open(IndexHtmlPath, 'w')
    IndexFileObj.write('<!DOCTYPE html>\n')
    IndexFileObj.write('<html lang="en">\n')
    IndexFileObj.write('\t<head>\n')
    IndexFileObj.write('\t\t<title>Year-Wise List</title>\n')
    IndexFileObj.write('\t</head>\n')
    IndexFileObj.write('\t<body>\n')
    IndexFileObj.write('\t\t<h1>Year-Wise List Of Issues<h1>\n')
    return IndexFileObj

def AddToIndexHtml(IndexFileObj, InputAnnualDir):
    IndexFileObj.write('\t\t<p><a href="%s/AnnualList.html">%s</a></p>\n' % (InputAnnualDir, InputAnnualDir))
    return IndexFileObj

def CloseIndexHtml(IndexFileObj):
    IndexFileObj.write('\t<body>\n')
    IndexFileObj.write('</html>\n')
    IndexFileObj.close()

def CloseAnnualList(AnnualFileObj):
    AnnualFileObj.write('\t\t<p><a href="../index.html">Back To Index</a></p>\n')
    AnnualFileObj.write('\t</body>\n')
    AnnualFileObj.write('</html>')
    AnnualFileObj.close()

def CloseMonthList(MonthFileObj):
    MonthFileObj.write('\t\t<p><a href="../../index.html">Back To Index</a></p>\n')
    MonthFileObj.write('\t\t<p><a href="../AnnualList.html">Back To Annual List</a></p>\n')
    MonthFileObj.write('\t</body>\n')
    MonthFileObj.write('</html>\n')
    MonthFileObj.close()

def MakeImageHtml(ImageHtmlPath, JpegMonthDir, ImageName, MaxPage):
    PageNumber = int(GetPageNumber(ImageName))
    f = open(ImageHtmlPath, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en"')
    f.write('\t<head>\n')
    f.write('\t\t<title>%s</title>\n' % (ImageName))
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<h1>%s</h1>\n' % (ImageName))
    f.write('\t\t<img src="../../JPEG_FILES/%s/%s.jpeg" alt="Image : %s">\n' % (JpegMonthDir, ImageName, ImageName))
    if PageNumber == 0:
        f.write('\t\t<p><a href="../%s.html">Previous</a></p>\n' % (JpegMonthDir))
    else:
        f.write('\t\t<p><a href="%s-%d.html">Previous</a></p>\n' % (JpegMonthDir, PageNumber - 1))
    if PageNumber == MaxPage:
        f.write('\t\t<p><a href="../../AnnualList.html">Next</a></p>\n')
    else:
        f.write('\t\t<p><a href="%s-%d.html">Next</a></p>\n' % (JpegMonthDir, PageNumber + 1))
    f.write('\t\t<p><a href="../../../index.html">Back To Index</a></p>\n')
    f.write('\t\t<p><a href="../../AnnualList.html">Back To Annual List</a></p>\n')
    f.write('\t\t<p><a href="../%s.html">Back To Month List</a></p>\n' % (JpegMonthDir))
    f.write('\t</body>\n')
    f.write('</html>\n')
    f.close()

def GetReadyAnnualList(AnnualListPath):
    f = open(AnnualListPath, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>Annual List</title>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<h1>List Of Monthly Issues</h1>\n')
    return f

def GetReadyMonthList(MonthListPath):
    f = open(MonthListPath, 'w')
    f.write('<DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>Month List</title>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<h1>List Of Pages Monthly Issues</h1>\n')
    return f

def AddToAnnualListHtml(AnnualFileObj, MonthDir):
    AnnualFileObj.write('\t\t<p><a href="HTML_FILES/%s.html">%s</a></p>\n' % (MonthDir, MonthDir))
    return AnnualFileObj

def AddToMonthListHtml(MonthFileobj, JpegMonthDir, ImageName):
    MonthFileobj.write('\t\t<p><a href="%s/%s.html">%s</a></p>\n' % (JpegMonthDir, ImageName, ImageName))
    return MonthFileobj

def MakeDir(DirPath):
    try:
        os.mkdir(DirPath)
    except FileExistsError:
        pass

def GetPageNumber(ImageName):
    list = ImageName.split('-')
    return list[len(list)-1]
