#!/bin/bash

zip -r docs/repository.webshare.zip repository.webshare

# shasum -a 1 docs/repository.webshare.zip > docs/repository.webshare.zip.md5

cp repository/addons.xml docs/addons.xml

md5sum repository/addons.xml | cut -d ' ' -f 1 > docs/addons.xml.md5
