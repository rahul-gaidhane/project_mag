import os
def genhtml(PAGE_NO, ISSUEMONTH, ISSUEYEAR):
    with open('newfile', 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n')
        f.write('   <head>\n')
        f.write('       <title>%s Issue Of %s</title>\n' % (ISSUEMONTH, ISSUEYEAR))
        f.write('       <meta charset="utf-8">\n')
        f.write('       <link rel="stylesheet" href="../../CSS/htmlcss.css">\n')
        f.write('       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">\n')
        f.write('       <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
        f.write('       <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>\n')
        f.write('       <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
        f.write('   </head>\n')
        f.write('   <body>\n')
        f.write('       <h6>Page %d: %s Issue Of %s</h6>\n' % (PAGE_NO,ISSUEMONTH, ISSUEYEAR))
        f.write('       <img src="...">\n')
        f.write('       <p><a href="...">Previous Page</a></p>\n')
        f.write('       <p><a href="...">Next Page</a></p>\n')
        f.write('       <p><a href="...">Back To Main</a></p>\n')
        f.write('       <p><a href="...">Back To Issue Main</a></p>\n')
        f.write('   </body>\n')
        f.write('</html>')


def GenImage(TIFF_FILENAME):
    """call imports() but it gave NameError:os not defined.why ?"""

    from PIL import Image
    FILENAME = GetFileName(TIFF_FILENAME)
    try:
        os.mkdir(FILENAME)
    except FileExistsError:
        pass
    img = Image.open(TIFF_FILENAME)
    os.chdir(FILENAME)
    for count in range(100):
        try:
            img.seek(count)
            img.save('%s-%d.jpg'%(FILENAME,count))
        except EOFError:
            break
    os.chdir('..')

def GetFileName(InputFilePath):
    return InputFilePath.split('/')[len(InputFilePath.split('/')) - 1]

def GenAnnualImages(InputDir):
    imports()
    InputDirList = os.listdir(InputDir)
    OutputPath = os.getcwd() + '1990-91'    '''1990-91 can be passed as argument'''
    os.mkdir(OutputPath)
    for MonthlyIssue in InputDirList:
        GenImage(InputDir + '/' + MonthlyIssue)



def Imports():
    print("In Imports:\n")
    import os
    from PIL import Image

def Main(InputPath, OutputPath):
    Imports()
    if OutputPath == '':
        OutputPath = os.getcwd + '/' + 'Output'
    else :
        OutputPath = OutputPath + '/' + 'Output'
    MainMain(InputPath,OutputPath)
        
def MainMain(InputPath, OutputPath):
    os.mkdir(OutputPath)
    genmainpage()   '''develope module to generate main html page'''
    InputDirList = os.listdir(InputPath)
    for year in InputDirList:
        OutputPath = OutputPath + '/' + year
        os.mkdir(OutputPath)
        InputPath = InputDir + '/' + year
        GenAnnualImages(InputPath)
