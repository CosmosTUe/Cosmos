for FILE in $(find . -name '*.html');
    do bootstrap-email $FILE > ".${FILE}"
done;