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


def genimage(TIFF_FILENAME):
"""call imports() but it gave NameError:os not defined.why ?"""
    import os
    from PIL import Image
    FILENAME = TIFF_FILENAME.split('.')[0]
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

def imports():
    print("imports is called")
    import os
    from PIL import Image
