#!/bin/bash

RELEASEDIR="ASIAGO-"$(date +%Y%m%d-%H%M%S)
mkdir $RELEASEDIR
cd ../Layout && sh zip_artwork.sh && cd -
cp ../Schematic/oh0.pdf $RELEASEDIR/ME0_ASIAGO_SCHEMATIC.pdf
cp ../Schematic/ME0_ASIAGO_BOM.xlsx $RELEASEDIR/
cp ../Layout/ME0_ASIAGO_ARTWORK.pdf $RELEASEDIR/
cp ../Layout/asiago_artwork.zip $RELEASEDIR/
zip -r asiago_project.zip ../Layout ../Schematic ../Padstacks ../Footprints && mv asiago_project.zip $RELEASEDIR/

cd $RELEASEDIR
mkdir ODB
tar xzvf ../../Layout/odbjob.tgz -C ./ODB/
zip -r asiago_odb.zip ODB
rm -r ODB
cd -

