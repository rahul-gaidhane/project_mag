#!/bin/sh
NUMBER_OF_ARGS=$#	#assigning names so that
#echo "NUMBER_OF_ARGS:$NUMBER_OF_ARGS"
INPUT_DIR=$1		#it will be easier to 
#echo "INPUT_DIR:$INPUT_DIR"
OUTPUT_DIR=$2		#understand the symbols and use its content more freely
#echo "OUTPUT_DIR:$OUTPUT_DIR"

if [ $NUMBER_OF_ARGS -eq 0 ] 	#checking for number of arguments passed 
then				#helps to execute the further program or to abort it.
	echo "ERROR:
1.PROVIDE ABSOLUTE OR RELATIVE PATH FOR DIRECTORY CONTAINING TIFF FILES.
2.PROVIDE ABSOLUTE OR RELATIVE PATH TO DIRECTORY FOR OUTPUT.[OPTIONAL]"
	exit
elif [ $NUMBER_OF_ARGS -eq 1 ] 		#even if one argument is passed instead of 
then					#two, event is handled by making an output directory.
	mkdir -p OUTPUT			#and creating the specified directories inside it.
	HTML_DIR=OUTPUT/HTML_FILES
	THUMBNAIL_DIR=OUTPUT/THUMBNAIL_FILES
	JPEG_DIR=OUTPUT/JPEG_FILES
elif [ $NUMBER_OF_ARGS -eq 2 ]
then
	JPEG_DIR=$OUTPUT_DIR/JPEG_FILES
	HTML_DIR=$OUTPUT_DIR/HTML_FILES
	THUMBNAIL_DIR=$OUTPUT_DIR/THUMBNAIL_FILES
else		# when more than two arguments are passed then to avoid confusion we exit the program execution
	echo "ERROR:			
1.PROVIDE ABSOLUTE OR RELATIVE PATH FOR DIRECTORY CONTAINING TIFF FILES.	
2.PROVIDE ABSOLUTE OR RELATIVE PATH TO DIRECTORY FOR OUTPUT.[OPTIONAL]
ONLY"
	exit
fi

#echo "JPEG_DIR:$JPEG_DIR"
#echo "HTML_DIR:$HTML_DIR"
#echo "THUMBNAIL_DIR:$THUMBNAIL_DIR"
 
INPUT_FILES_LIST=`ls $INPUT_DIR`	#contains list of files for which HTML pages are to be generated
#echo "INPUT_FILES_LIST:$INPUT_FILES_LIST"

mkdir -p $HTML_DIR $JPEG_DIR $THUMBNAIL_DIR	#create the specified directories to store output

> $HTML_DIR/main_page.html 	#creates main_page.html inside html directory, which lists all the issues
echo "<!DOCTYPE html>
<html>
	<head>
		<title>LIST OF ISSUES BETWEEN 1990-1991</title>
	</head>
	<body>
		" > $HTML_DIR/main_page.html
for INPUT_FILENAME in $INPUT_FILES_LIST		#using loop we convert each INPUT_FILENAME into jpeg images
do						#we use loop to repeat some specific tasks for each file.
#	echo "INPUT_FILENAME:$INPUT_FILENAME"
	INPUT_FILETYPE=`file $INPUT_DIR/$INPUT_FILENAME | cut -d' ' -f 2`
#	echo "INPUT_FILETYPE:$INPUT_FILETYPE" 
	if [ "$INPUT_FILETYPE" = "TIFF" ]	#we identify type of file and adjust the code to make program 
	then 					#generic in terms of its use.
		ISSUEOF=`basename $INPUT_FILENAME .tif`
	elif [ "$INPUT_FILETYPE" = "PDF" ]	
	then
		ISSUEOF=`basename $INPUT_FILENAME .pdf`	#oh I hate this name "ISSUEOF"
	else				#exit program when an file of inapropriate file type is supplied
		echo "ERROR:NOT AN APPROPRIATE FILE TYPE"
		exit
	fi
#	echo "ISSUEOF:$ISSUEOF"	
# 	creates each individual file for each issue 

	> $HTML_DIR/$ISSUEOF.html	#create an individual HTML file for issue
	echo "<!DOCTYPE html>
<html>
	<head>
		<title>$ISSUEOF</title>	
	</head>
	<body>
		"> $HTML_DIR/$ISSUEOF.html

	mkdir -p $JPEG_DIR/$ISSUEOF		#creating directory by the name consisting of month and year of 
	mkdir -p $HTML_DIR/$ISSUEOF		#issue to keep all the files of a particular issue in groups
	mkdir -p $THUMBNAIL_DIR/$ISSUEOF	

	# for each file of an issue jpeg files are to be generated and kept in jpeg_dir within specific directory 
	# of a particular issue.
	convert -trim -density 200 $INPUT_DIR/$INPUT_FILENAME -quality 100 $JPEG_DIR/$ISSUEOF/$ISSUEOF.jpeg 2>/dev/null

	for JPEG_FILENAME in `ls $JPEG_DIR/$ISSUEOF`	#loop is used to generate a html file per image.
	do						
#		echo "JPEG_FILENAME:$JPEG_FILENAME"
		
		JPEG_NAME=`basename $JPEG_FILENAME .jpeg`	#using jpeg_name we make HTML_FILENAME and
		HTML_FILENAME=$JPEG_NAME.html			#THUMBNAIL_FILENAME so that files can be created
		THUMBNAIL_FILENAME=$JPEG_NAME.jpeg		# by that name.
		
		#generating thumbnails out of each jpeg image using convert command
		convert -trim $JPEG_DIR/$ISSUEOF/$JPEG_FILENAME -resize 300 -quality 100 $THUMBNAIL_DIR/$ISSUEOF/$THUMBNAIL_FILENAME
		# creating links to each html_page of an issue
#		echo "<p><a href=\"$ISSUEOF/$HTML_FILENAME\"><img src=\"../THUMBNAIL_FILES/$ISSUEOF/$THUMBNAIL_FILENAME\" alt=\"THUMBNAIL FOR $JPEG_NAME\">$JPEG_NAME</a></p>" >> $HTML_DIR/$ISSUEOF.html	

#		echo "JPEG_NAME:$JPEG_NAME"
#		echo "HTML_FILENAME:$HTML_FILENAME"

		PAGE_NO=`basename $JPEG_FILENAME .jpeg | awk -F- '{print $NF+1}'`	#getting page number from
											#jpeg_filename
		MAX_PAGE=`ls $JPEG_DIR/$ISSUEOF | wc -l`	#counting the number of files in issue directory
	
#		creates individual html files for each page
		
		> $HTML_DIR/$ISSUEOF/$HTML_FILENAME	#creating html file for each image
		echo "<!DOCTYPE html>
	<html>
		<head>
			<title>PAGE $PAGE_NO</title>
		</head>
		<body>
			<img src=\"../../JPEG_FILES/$ISSUEOF/$JPEG_FILENAME\" alt=$JPEG_NAME>
">>$HTML_DIR/$ISSUEOF/$HTML_FILENAME
			if [ $PAGE_NO -eq 1 ] 
			then
				echo "		<p><a href=\"../main_page.html\">PREVIOUS PAGE</a></p>">> $HTML_DIR/$ISSUEOF/$HTML_FILENAME
			else
				PREVIOUS_PAGE=`expr $PAGE_NO - 2`
				echo "		<p><a href=\"$ISSUEOF-$PREVIOUS_PAGE.html\">PREVIOUS PAGE</a></p>">> $HTML_DIR/$ISSUEOF/$HTML_FILENAME
			fi
#			echo "MAX_PAGE:$MAX_PAGE"
#			echo "PAGE_NO:$PAGE_NO"
			if [ $PAGE_NO = $MAX_PAGE ]
			then
				echo "
		<p><a href=\"../main_page.html\">NEXT PAGE</a></p>">>$HTML_DIR/$ISSUEOF/$HTML_FILENAME
			else
			echo "
		<p><a href=\"$ISSUEOF-$PAGE_NO.html\">NEXT PAGE</a></p>">>$HTML_DIR/$ISSUEOF/$HTML_FILENAME
			fi
		echo "
		<p><a href=\"../main_page.html\">BACK TO MAIN</a></p>
		<p><a href=\"../$ISSUEOF.html\">BACK TO ISSUE MENU</a></p>
	</body>
</html>">> $HTML_DIR/$ISSUEOF/$HTML_FILENAME	#SINGLE FILE IS GENERATED FOR EACH IMAGE
	 done
	echo "ISSUEOF:$ISSUEOF"
	echo "MAX_PAGE:$MAX_PAGE"
	echo "PAGE_NO:$PAGE_NO"
	for ((number=0; number < $MAX_PAGE; number++))
	{
		echo "<p><a href=\"$ISSUEOF/$ISSUEOF-$number.html\"><img src=\"../THUMBNAIL_FILES/$ISSUEOF/$ISSUEOF-$number.jpeg\" alt=\"THUMBNAIL FOR $JPEG_NAME\">$ISSUEOF-$number</a></p>" >> $HTML_DIR/$ISSUEOF.html	
	}
	echo "			<p><a href=\"main_page.html\">BACK TO MAIN</a></p>	
	</body>
</html>" >> $HTML_DIR/$ISSUEOF.html	#single file for each issue is generated
	#list of issues is put on main page
	echo "<p><a href=\"$ISSUEOF.html\">Issue of $ISSUEOF</a></p>" >> $HTML_DIR/main_page.html
done 
	echo "	</body>
</html>" >> $HTML_DIR/main_page.html 	#main file is generated at last.
exit
