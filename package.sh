#!/bin/bash

VERSION=$(cat ./VERSION);

STAGING_FOLDER="deluge-kodi-plugin-${VERSION}"
ZIP="package/${VERSION}.zip"

if [ ! -d "./package" ]
then
    mkdir ./package;
fi

rm -rf $STAGING_FOLDER;
rm -rf $ZIP;

mkdir $STAGING_FOLDER
for FILE in resources addon.xml default.py icon.png;
do
    cp -a $FILE $STAGING_FOLDER;
done;

sed -i -E "s/^(\s+version)=\"[0-9\.]+\"/\1=\"${VERSION}\"/" addon.xml

zip -rq $ZIP $STAGING_FOLDER;
rm -rf $STAGING_FOLDER;

echo "New package at ${ZIP}"