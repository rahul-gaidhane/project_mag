import os
from PIL import Image
import magic #use "pip3 install python-magic" command to install magic library
import subprocess
import logging

##
def main(InputDir, OutputDir):
    if not OutputDir:
        OutputDir = os.path.join(os.getcwd(), 'Output')
    else:
        OutputDir = os.path.join(OutputDir, 'Output')
    logging.basicConfig(level=logging.DEBUG)
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
    logging.info("Inside GenMetaFiles:")
    logging.debug("OutputDirPath = %s" % (OutputDirPath))

def GenJpegThumbImages(ArchiveDirPath, OutputDirPath):
    logging.info("Inside GenJpegThumbImages:")
    logging.debug("ArchiveDirPath = %s\n" % (ArchiveDirPath))
    logging.debug("OutputDirPath = %s\n" % (OutputDirPath))
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
            logging.warning("FileTypeError : In apropriate File detected\nFilePath = %s" % (ArchiveFilePath))

def GenHtmlFiles(OutputDirPath):
    logging.info("Inside GenHtmlFiles:")
    logging.debug("OutputDirPath = %s\n" % (OutputDirPath))
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
    IndexFileObj.write('\t\t<title>आजचा सुधारक</title>\n')
    IndexFileObj.write('\t\t<meta charset="utf-8">\n')
    IndexFileObj.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    IndexFileObj.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    IndexFileObj.write('\t\t<link rel="stylesheet" href="CSS/IndexCss.css">\n')
    IndexFileObj.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    IndexFileObj.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    IndexFileObj.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    IndexFileObj.write('\t</head>\n')
    IndexFileObj.write('\t<body>\n')
    IndexFileObj.write('\t\t<div class="container">\n')
    IndexFileObj.write('\t\t\t<h3 class="display-1">AAjcha Sudharak</h3>\n')
    IndexFileObj.write('\t\t\t<div class="list-group">\n')
    return IndexFileObj

def AddToIndexHtml(IndexFileObj, InputAnnualDir):
    IndexFileObj.write('\t\t\t\t<a class="list-group-item text-center list-group-item-action" href="%s/AnnualList.html">%s</a>\n' % (InputAnnualDir, InputAnnualDir))
    return IndexFileObj

def CloseIndexHtml(IndexFileObj):
    IndexFileObj.write('\t\t\t</div>\n')
    IndexFileObj.write('\t\t</div>\n')
    IndexFileObj.write('\t</body>\n')
    IndexFileObj.write('</html>\n')
    IndexFileObj.close()

def CloseAnnualList(AnnualFileObj):
    AnnualFileObj.write('\t\t</div>\n')
    AnnualFileObj.write('\t\t<a class="btn btn-primary" href="../index.html">Back To Index</a>\n')
    AnnualFileObj.write('\t</div>\n')
    AnnualFileObj.write('\t</body>\n')
    AnnualFileObj.write('</html>')
    AnnualFileObj.close()

def CloseMonthList(MonthFileObj):
    MonthFileObj.write('\t\t\t</div>\n')
    MonthFileObj.write('\t\t\t<a class="btn btn-primary" href="../../index.html">Back To Index</a>\n')
    MonthFileObj.write('\t\t\t<a class="btn btn-primary" href="../AnnualList.html">Back To Annual List</a>\n')
    MonthFileObj.write('\t\t</div>\n')
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
    f.write('\t\t<div class="container">\n')
    f.write('\t\t\t<h4 class="text-center display-4">Page %d : %s</h4>\n' % (PageNumber + 1, JpegMonthDir))
    f.write('\t\t\t<img class="img-fluid" src="../../JPEG_FILES/%s/%s.jpeg" alt="Image : %s"><br>\n' % (JpegMonthDir, ImageName, ImageName))
    if PageNumber == 0:
        f.write('\t\t\t<a class="btn btn-primary" href="../%s.html">PREVIOUS</a>\n' % (JpegMonthDir))
    else:
        f.write('\t\t\t<a class="btn btn-primary" href="%s-%d.html">PREVIOUS</a>\n' % (JpegMonthDir, PageNumber - 1))
    if PageNumber == MaxPage:
        f.write('\t\t\t<a class="btn btn-primary" href="../../AnnualList.html">NEXT</a>\n')
    else:
        f.write('\t\t\t<a class="btn btn-primary" href="%s-%d.html">NEXT</a>\n' % (JpegMonthDir, PageNumber + 1))
    f.write('\t\t\t<a class="btn btn-primary" href="../../../index.html">HOME</a>\n')
    f.write('\t\t\t<a class="btn btn-primary" href="../../AnnualList.html">ANNUAL LIST</a>\n')
    f.write('\t\t\t<a class="btn btn-primary" href="../%s.html">MONTH LIST</a>\n' % (JpegMonthDir))
    f.write('\t\t</div>')
    f.write('\t</body>\n')
    f.write('</html>\n')
    f.close()

def GetReadyAnnualList(AnnualListPath):
    f = open(AnnualListPath, 'w')
    #updated logic
    year = AnnualListPath.split('/')[-2]
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>%s List</title>\n' % (year))
    f.write('\t\t<meta charset="utf-8">\n')
    f.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    f.write('\t\t<link rel="stylesheet" href="../CSS/AnnualListCss.css">\n')
    f.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    f.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<div class="container">\n')
    f.write('\t\t<h1>List Of %s Issues</h1>\n' % (year))
    f.write('\t\t\t<div class="list-group">\n')
    return f

def GetReadyMonthList(MonthListPath):
    f = open(MonthListPath, 'w')
    #updated code
    month = os.path.basename(MonthListPath).split('.')[0]
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n')
    f.write('\t<head>\n')
    f.write('\t\t<title>%s Issue</title>\n' % (month))
    f.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
    f.write('\t\t<link rel="stylesheet" href="../../CSS/MonthListCss.css">\n')
    f.write('\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
    f.write('\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
    f.write('\t</head>\n')
    f.write('\t<body>\n')
    f.write('\t\t<div class="container">\n')
    f.write('\t\t\t<h1>%s Issue</h1>\n' % (month))
    f.write('\t\t\t<div class="row">\n')
    return f

def AddToAnnualListHtml(AnnualFileObj, MonthDir):
    AnnualFileObj.write('\t\t\t\t<a class="list-group-item text-center list-group-item-action" href="HTML_FILES/%s.html">%s</a>\n' % (MonthDir, MonthDir))
    return AnnualFileObj

def AddToMonthListHtml(MonthFileObj, JpegMonthDir, ImageName):
    PageNumber = int(GetPageNumber(ImageName))
    MonthFileObj.write('\t\t\t\t<div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 col-12">\n')
    MonthFileObj.write('\t\t\t\t\t<a href="%s/%s.html"><img class="img-fluid" src="../THUMBNAIL_FILES/%s/%s.jpeg" alt="%d Thumbnail"></a>\n' % (JpegMonthDir, ImageName, JpegMonthDir, ImageName, PageNumber))
    MonthFileObj.write('\t\t\t\t\t<p>Page %d</p>\n' % (PageNumber))
    MonthFileObj.write('\t\t\t\t</div>\n')
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
