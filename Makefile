# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only intended for developers.
#       It is only meant for UNIX-like operating systems.
#       Most of the commands require extra software.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2022-02-02T23:43:39+0100
.PHONY: clean check format test doc zip

PROJECT:=examples

.if make(zip)
TAGCOMMIT!=git rev-list --tags --max-count=1
TAG!=git describe --tags ${TAGCOMMIT}
.endif

all::
	@echo 'you can use the following commands:'
	@echo '* clean: remove all generated files.'
	@echo '* check: check all python files. (requires pylama)'
	@echo '* tags: regenerate tags file. (requires uctags)'
	@echo '* format: format the source. (requires black)'
#	@echo '* test: run the built-in tests. (requires py.test)'
#	@echo '* zip: create a zipfile of the latest tagged version.'

# Remove generated files.
clean::
	rm -f backup-*.tar* ${PROJECT}-*.zip
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# Run the pylama code checker
check:: .IGNORE
	pylama *.py *.pyw

# Regenerate tags file.
tags::
	uctags -R --languages=Python

# Reformat all source code using black
format::
	black --include '.*\.pyw' .

# Run the test suite
#test::
#	py.test -v

# Create a zip-file from the most recent tagged state of the repository.
zip:: clean
	cd doc && make clean
	git checkout ${TAG}
	cd .. && zip -r ${PROJECT}-${TAG}.zip ${PROJECT} \
		-x '*/.git/*' '*/.pytest_cache/*' '*/__pycache__/*' '*/.cache/*'
	git checkout main
	mv ../${PROJECT}-${TAG}.zip .
