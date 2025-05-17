#!/bin/bash

zip -r repository.zip repository

shasum -a 1 repository.zip > repository.zip.md5
