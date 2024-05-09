# file: Makefile
# vim:fileencoding=utf-8:ft=make
#
# NOTE: This Makefile is only intended for developers.
#       It is only meant for UNIX-like operating systems.
#       Most of the commands require extra software.
#       Building the documentation requires a working LaTeX/docutils installation.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2024-05-09T22:04:27+0200
.POSIX:
.SUFFIXES:
.PHONY: clean check tags format doc zip working-tree-clean 

PROJECT:=python-examples

# For a Python program, help is the default target.
help::
	@echo "Command  Meaning"
	@echo "-------  -------"
	@sed -n -e '/##/s/:.*\#\#/\t/p' -e '/@sed/d' Makefile

clean:: ## remove all generated files.
	rm -f backup-*.tar* ${PROJECT}-*.zip
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

.ifmake check || format
FILES!=find . -type f -name '*.py*'
.endif
check:: .IGNORE ## check all python files. (requires pylama)
	pylama ${FILES}

tags:: ## regenerate tags file. (requires uctags)
	uctags -R --languages=Python

format:: ## format the source. (requires black)
	black ${FILES}

.ifmake zip
TAGCOMMIT!=git rev-list --tags --max-count=1
TAG!=git describe --tags ${TAGCOMMIT}
.endif
zip:: clean working-tree-clean ## create a zip-file from the most recent tagged state of the repository.
	git checkout ${TAG}
	cd .. && zip -r ${PROJECT}-${TAG}.zip ${PROJECT} \
		-x '*/.git/*' '*/.pytest_cache/*' '*/__pycache__/*' '*/.cache/*'
	git checkout main
	mv ../${PROJECT}-${TAG}.zip .

working-tree-clean:: ## check if the working tree is clean. (requires git)
	git status | grep -q 'working tree clean'
