import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library
import subprocess


def main(InputDir, OutputDir):
    if not OutputDir:
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

def GenJpegThumbImages(ArchiveDirPath, OutputDirPath)
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
        MonthFileObj = MakeMonthList(MonthFileObj, JpegMonthDir, MaxPage+1)
        for ImageFile in JpegMonthImageList:
            ImageName = os.path.splitext(ImageFile)[0]
            #MonthFileObj = AddToMonthListHtml(MonthFileObj, JpegMonthDir, ImageName)
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
    IndexFileObj.write('\t\t<meta charset="utf-8"\n')
    IndexFileObj.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    IndexFileObj.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    IndexFileObj.write('\t\t<link rel="stylesheet" href="CSS/IndexCss.html"\n')
    IndexFileObj.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    IndexFileObj.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    IndexFileObj.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    IndexFileObj.write('\t</head>\n')
    IndexFileObj.write('\t<body>\n')
    IndexFileObj.write('\t\t<h3>Year-Wise List Of Issues</h3>\n')
    return IndexFileObj

def AddToIndexHtml(IndexFileObj, InputAnnualDir):
    IndexFileObj.write('\t\t<p><a href="%s/AnnualList.html">%s</a></p>\n' % (InputAnnualDir, InputAnnualDir))
    return IndexFileObj

def CloseIndexHtml(IndexFileObj):
    IndexFileObj.write('\t</body>\n')
    IndexFileObj.write('</html>\n')
    IndexFileObj.close()

def CloseAnnualList(AnnualFileObj):
    AnnualFileObj.write('\t\t<p><a href="../index.html">Back To Index</a></p>\n')
    AnnualFileObj.write('\t</body>\n')
    AnnualFileObj.write('</html>')
    AnnualFileObj.close()

def CloseMonthList(MonthFileObj):
    MonthFileObj.write('\t</div>\n')
    MonthFileObj.write('\t</div>\n')
    MonthFileObj.write('\t<p><a href="../../index.html">Back To Index</a></p>\n')
    MonthFileObj.write('\t<p><a href="../AnnualList.html">Back To Annual List</a></p>\n')
    MonthFileObj.write('\t</body>\n')
    MonthFileObj.write('</html>\n')
    MonthFileObj.close()

def MakeImageHtml(ImageHtmlPath, JpegMonthDir, ImageName, MaxPage):
    PageNumber = int(GetPageNumber(ImageName))
    f = open(ImageHtmlPath, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en"')
    f.write('\t<head>\n')
    f.write('\t\t<title>Page %d : %s</title>\n' % (PageNumber, JpegMonthDir))
    f.write('\t\t<meta charset="utf-8">\n')
    f.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    f.write('\t\t<link rel="stylesheet" href="../../../CSS/HtmlCss.css">\n')
    f.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    f.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<h4>Page %d : %s</h4>\n' % (PageNumber + 1, JpegMonthDir))
    f.write('\t\t<img src="../../JPEG_FILES/%s/%s.jpeg" alt="Image : %s">\n' % (JpegMonthDir, ImageName, ImageName))
    if PageNumber == 0:
        f.write('\t\t<p><a href="../%s.html"><< PREVIOUS</a></p>\n' % (JpegMonthDir))
    else:
        f.write('\t\t<p><a href="%s-%d.html"><< PREVIOUS</a></p>\n' % (JpegMonthDir, PageNumber - 1))
    if PageNumber == MaxPage:
        f.write('\t\t<p><a href="../../AnnualList.html">NEXT >></a></p>\n')
    else:
        f.write('\t\t<p><a href="%s-%d.html">NEXT >></a></p>\n' % (JpegMonthDir, PageNumber + 1))
    f.write('\t\t<p><a href="../../../index.html">HOME</a></p>\n')
    f.write('\t\t<p><a href="../../AnnualList.html">ANNUAL LIST</a></p>\n')
    f.write('\t\t<p><a href="../%s.html">MONTH LIST</a></p>\n' % (JpegMonthDir))
    f.write('\t</body>\n')
    f.write('</html>\n')
    f.close()

def GetReadyAnnualList(AnnualListPath):
    f = open(AnnualListPath, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>Annual List</title>\n')
    f.write('\t\t<meta charset="utf-8">\n')
    f.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    f.write('\t\t<link rel="stylesheet" href="../CSS/AnnualListCss.css">\n')
    f.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    f.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    #f.write('\t\t<div class="container">\n')
    f.write('\t\t<h1>List Of Monthly Issues</h1>\n')
    #f.write('\t\t<div class="row">\n')
    return f

def GetReadyMonthList(MonthListPath):
    f = open(MonthListPath, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>Month List</title>\n')
    f.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    f.write('\t\t<link rel="stylesheet" href="../../CSS/MonthListCss.css">\n')
    f.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    f.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<div class="container">\n')
    f.write('\t\t<h1>List Of Pages Monthly Issues</h1>\n')
    f.write('\t\t<div class="row">\n')
    return f

def AddToAnnualListHtml(AnnualFileObj, MonthDir):
    AnnualFileObj.write('\t\t\t<p><a href="HTML_FILES/%s.html">%s</a></p>\n' % (MonthDir, MonthDir))
    return AnnualFileObj

def AddToMonthListHtml(MonthFileObj, JpegMonthDir, ImageName):
    PageNumber = int(GetPageNumber(ImageName))
    MonthFileObj.write('\t\t<div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 col-12">\n')
    MonthFileObj.write('\t\t\t<a href="%s/%s.html"><img class="img-fluid" src="../THUMBNAIL_FILES/%s/%s.jpeg" alt="%d Thumbnail"></a>\n' % (JpegMonthDir, ImageName, JpegMonthDir, ImageName, PageNumber))
    MonthFileObj.write('\t\t\t<p>Page %d</p>\n' % (PageNumber))
    MonthFileObj.write('\t\t</div>\n')
    return MonthFileObj

def MakeMonthList(MonthFileObj, JpegMonthDir, MaxPage):
    for count in range(MaxPage):
        PageNumber = count + 1
        ImageName = JpegMonthDir + '-' + str(count)
        MonthFileObj.write('\t\t<div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 col-12">\n')
        MonthFileObj.write('\t\t\t<a href="%s/%s.html"><img class="img-fluid" src="../THUMBNAIL_FILES/%s/%s.jpeg" alt="%d Thumbnail"></a>\n' % (JpegMonthDir, ImageName, JpegMonthDir, ImageName, PageNumber))
        MonthFileObj.write('\t\t\t<p>Page %d</p>\n' % (PageNumber))
        MonthFileObj.write('\t\t</div>\n')
    return MonthFileObj

def MakeDir(DirPath):
    try:
        os.mkdir(DirPath)
    except FileExistsError:
        pass

def GetPageNumber(ImageName):
    list = ImageName.split('-')
    return list[len(list)-1]
