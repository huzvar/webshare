#!/bin/bash

zip -r docs/repository.zip repository

shasum -a 1 docs/repository.zip > docs/repository.zip.md5
