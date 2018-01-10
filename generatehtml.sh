#!/bin/sh
if [ $# -eq 0 ] 
then
	echo "ERROR:
1.PROVIDE ABSOLUTE OR RELATIVE PATH FOR DIRECTORY CONTAINING TIFF FILES.
2.PROVIDE ABSOLUTE OR RELATIVE PATH TO DIRECTORY FOR OUTPUT.[OPTIONAL]"
	exit
elif [ $# -eq 1 ] 
then
	mkdir -p OUTPUT
	HTML_PATH=OUTPUT/HTML_FILES
	THUMB_PATH=OUTPUT/THUMB_FILES
	JPEG_PATH=OUTPUT/JPEG_FILES
elif [ $# -eq 2 ]
then
	JPEG_PATH=$2/JPEG_FILES
	HTML_PATH=$2/HTML_FILES
	THUMB_PATH=$2/THUMB_FILES
else
	echo "ERROR:
1.PROVIDE ABSOLUTE OR RELATIVE PATH FOR DIRECTORY CONTAINING TIFF FILES.
2.PROVIDE ABSOLUTE OR RELATIVE PATH TO DIRECTORY FOR OUTPUT.[OPTIONAL]
ONLY"
	exit
fi
 
SOURCE_FILES=`ls $1`	#contains list of files 

mkdir -p $HTML_PATH $JPEG_PATH $THUMB_PATH

# creates main html which lists all the issues

> $HTML_PATH/main.html
echo "<!DOCTYPE html>
<html>
	<head>
		<title>LIST OF ISSUES BETWEEN 1990-1991</title>
	</head>
	<body>
		" > $HTML_PATH/main.html
for SOURCE_FILENAME in $SOURCE_FILES
do
	FILETYPE=`file $1/$SOURCE_FILENAME | cut -d ' ' -f 2`
#	echo "FILETYPE:$FILETYPE" 
	if [ "$FILETYPE" = "TIFF" ]
	then 
		ISSUENAME=`basename $SOURCE_FILENAME .tif`
	elif [ "$FILETYPE" = "PDF" ]
	then
		ISSUENAME=`basename $SOURCE_FILENAME .pdf`
	else
		echo "ERROR:NOT AN APPROPRIATE FILE TYPE"
	fi
	
# 	creates each individual file for each issue 

	> $HTML_PATH/$ISSUENAME.html
	echo "<!DOCTYPE html>
<html>
	<head>
		<title>$ISSUENAME</title>
	</head>
	<body>
		"> $HTML_PATH/$ISSUENAME.html

	mkdir -p $JPEG_PATH/$ISSUENAME
	mkdir -p $HTML_PATH/$ISSUENAME
	mkdir -p $THUMB_PATH/$ISSUENAME

	convert $1/$SOURCE_FILENAME $JPEG_PATH/$ISSUENAME/$ISSUENAME.jpeg 2>/dev/null

	for JPEG_FILENAME in `ls $JPEG_PATH/$ISSUENAME`
	do
#		echo "JPEG_FILENAME:$JPEG_FILENAME"
		
		JPEG_PER_PAGE=`basename $JPEG_FILENAME .jpeg`
		HTML_PER_PAGE=$JPEG_PER_PAGE.html
		THUMB_PER_PAGE=$JPEG_PER_PAGE.jpeg
		
		convert -density 300 $JPEG_PATH/$ISSUENAME/$JPEG_FILENAME -resize 300 -quality 100 $THUMB_PATH/$ISSUENAME/$THUMB_PER_PAGE
		echo "<p><a href=\"$ISSUENAME/$HTML_PER_PAGE\"><img src=\"../THUMB_FILES/$ISSUENAME/$THUMB_PER_PAGE\" alt=\"$JPEG_PER_PAGE\">$JPEG_PER_PAGE</a></p>" >> $HTML_PATH/$ISSUENAME.html	
#		echo "JPEG_PER_PAGE:$JPEG_PER_PAGE"
#		echo "HTML_PER_PAGE:$HTML_PER_PAGE"
		PAGE_NO=`basename $JPEG_FILENAME .jpeg | awk -F- '{print $NF+1}'`
#		creates individual html files for each page
		
		> $HTML_PATH/$ISSUENAME/$HTML_PER_PAGE
		echo "<!DOCTYPE html>
	<html>
		<head>
			<title>PAGE $PAGE_NO</title>
		</head>
		<body>
			<img src=\"../../JPEG_FILES/$ISSUENAME/$JPEG_FILENAME\" alt=$JPEG_PER_PAGE>
			<p><a href=\"../main.html\">BACK TO MAIN</a></p>
			<p><a href=\"../$ISSUENAME.html\">BACK TO ISSUE MENU</a></p>
		</body>
	</html>" >> $HTML_PATH/$ISSUENAME/$HTML_PER_PAGE
	 done
	echo "			<p><a href=\"main.html\">BACK TO MAIN</a></p>
	</body>
</html>" >> $HTML_PATH/$ISSUENAME.html
	
	echo "<p><a href=\"$ISSUENAME.html\">Issue of $ISSUENAME</a></p>" >> $HTML_PATH/main.html
done 
	echo "	</body>
</html>" >> $HTML_PATH/main.html
exit
