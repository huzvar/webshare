#!/bin/bash

rm docs/repository.webshare.zip
zip -r docs/repository.webshare.zip repository.webshare

# shasum -a 1 docs/repository.webshare.zip > docs/repository.webshare.zip.md5

cd repository

cp addons.xml ../docs/addons.xml
md5sum addons.xml > ../docs/addons.xml.md5

VERSION=`awk -F'version="' '/<addon/{split($2,a,"\""); print a[1]}' plugin.video.webshare/addon.xml`
rm ../docs/plugin.video.webshare/plugin.video.webshare-${VERSION}.zip
zip -r ../docs/plugin.video.webshare/plugin.video.webshare-${VERSION}.zip plugin.video.webshare
