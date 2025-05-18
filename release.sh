#!/bin/bash

# rm docs/repository.webshare.zip
# zip -r docs/repository.webshare.zip repository.webshare

cd repository

# cp addons.xml ../docs/addons.xml
# md5sum addons.xml > ../docs/addons.xml.md5

# VERSION=`awk -F'version="' '/<addon/{split($2,a,"\""); print a[1]}' plugin.video.webshare/addon.xml`
# rm ../docs/plugin.video.webshare/plugin.video.webshare-${VERSION}.zip
# zip -r ../docs/plugin.video.webshare/plugin.video.webshare-${VERSION}.zip plugin.video.webshare


zip -r ../docs/plugin.video.webshare.zip plugin.video.webshare
