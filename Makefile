# file: Makefile
# vim:fileencoding=utf-8:ft=make
#
# NOTE: This Makefile is only intended for developers.
#       It is only meant for UNIX-like operating systems.
#       Most of the commands require extra software.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2024-01-21T17:41:49+0100
.POSIX:
.PHONY: clean check format test zip working-tree-clean
.SUFFIXES:

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

FILES!=find . -type f -name '*.py*'
check:: .IGNORE ## check all python files. (requires pylama)
	pylama ${FILES}

tags:: ## regenerate tags file. (requires uctags)
	uctags -R --languages=Python

format:: ## format the source. (requires black)
	black ${FILES}

# test:: ## run the built-in tests. (requires py.test)
# 	py.test -v

.ifmake zip
#TAGCOMMIT!=git rev-list --tags --max-count=1
#TAG!=git describe --tags ${TAGCOMMIT}
TAG!=date -u '+%Y%m%dT%H%M%SZ'
.endif
zip:: clean ## create a zip-file from the most recent tagged state of the repository.
#	git checkout ${TAG}
	cd .. && zip -r ${PROJECT}-${TAG}.zip ${PROJECT} \
		-x '*/.git/*' '*/.pytest_cache/*' '*/__pycache__/*' '*/.cache/*'
#	git checkout main
	mv ../${PROJECT}-${TAG}.zip .

working-tree-clean:: ## check if the working tree is clean. (requires git)
	git status | grep -q 'working tree clean'
