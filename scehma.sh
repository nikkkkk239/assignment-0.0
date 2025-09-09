#!/bin/bash


curl -s https://www.amfiindia.com/spages/NAVAll.txt -o NAVAll.txt

awk -F ';' 'NR>1 && $4 != "" && $5 != "" {print $4 "\t" $5}' NAVAll.txt > scheme_nav.tsv

echo "Extracted Scheme Name and Asset Value into scheme_nav.tsv"
