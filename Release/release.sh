#!/bin/bash

DATESHORT=$(date +%Y%m%d)
RELEASEDIR="ASIAGO-"$(date +%Y%m%d-%H%M%S)
mkdir $RELEASEDIR
cd ../Layout && sh zip_artwork.sh && cd -
cp ../Schematic/oh0.pdf $RELEASEDIR/me0_asiago_schematic_$DATESHORT.pdf
cp ../Layout/place_txt.txt $RELEASEDIR/me0_asiago_placement_$DATESHORT.txt
cp ../Schematic/ME0_ASIAGO_BOM.xlsx $RELEASEDIR/me0_asiago_bom_$DATESHORT.xlsx
cp ../Layout/ME0_ASIAGO_ARTWORK.pdf $RELEASEDIR/me0_asiago_artwork_$DATESHORT.pdf
cp ../Layout/asiago_artwork.zip $RELEASEDIR/me0_asiago_artwork_$DATESHORT.zip
zip -FS -r asiago_project.zip ../Layout ../Schematic ../Padstacks ../Footprints && mv asiago_project.zip $RELEASEDIR/me0_asiago_project_$DATESHORT.zip

cd $RELEASEDIR
mkdir ODB
tar xzvf ../../Layout/odbjob.tgz -C ./ODB/
zip -FS -r me0_asiago_odb_$DATESHORT.zip ODB
rm -r ODB
cd -

