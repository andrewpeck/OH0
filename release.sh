#!/bin/bash

RELEASEDIR = "ASIAGO-"$(date +%Y-%m-%d-%H%M%S)
mkdir $RELEASEDIR
cp ../Schematic/oh0.pdf $RELEASEDIR/
cp ../Schematic/ME0_ASIAGO_BOM.xlsx $RELEASEDIR/
cp ../Layout/ME0_ASIAGO_ARTWORK.pdf $RELEASEDIR/
cp ../Layout/asiago_artwork.zip $RELEASEDIR/
zip asiago_project.zip ../Layout ../Schematic ../Padstacks ../Footprints && mv asiago_project $RELEASEDIR/
