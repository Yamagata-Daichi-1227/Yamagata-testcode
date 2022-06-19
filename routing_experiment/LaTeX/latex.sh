#!/bin/bash

set -e

if [ $# -ne 1 ]; then
	echo "please type title of your LaTeX text. \n"
	exit 1
fi

platex -halt-on-error -interaction=nonstopmode -file-line-error $1.tex
platex -halt-on-error -interaction=nonstopmode -file-line-error $1.tex | sed -r "s/Error|Warnings?/\x1b[33m\0\x1b[0m/gi"
dvipdfmx $1.dvi
evince $1.pdf
rm $1.aux $1.dvi $1.log
