#!/usr/bin/env sh

mkdir Raya;
cp __init__.py Raya/__init__.py;
zip Raya.zip ./Raya/*;
rm -rf Raya;