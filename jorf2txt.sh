f=$1
min=$2
max=$3

# conversion en PDF vers TIFF multipage
convert -density 300 "$f[$min-$max]" -rotate 90 -background white +matte -crop 2850x2000+250+250 -alpha off -depth 8 "$f.tiff"

# conversion en TIFF monopage
convert "$f.tiff" $f-%02d.tiff

rm -f $f.txt
for p in $f-*.tiff
do
    echo $p
    # OCR avec tesseract
    tesseract $p stdout -l fra --psm 1 >> "$f.tmp"
done

cat $f.tmp \
 | sed "s/’/'/g;s/‘/'/g;s/“/\"/g;s/”/\"/g" \
 | sed 's"!"/"g;s"l"/"g;s/^N$//' \
> $f.csv

rm *.tiff
rm *.tmp
