default: help

NAME=janitor
MAN=janitor.1
VERSION=0.5
RPMDIST=$(shell rpm --eval '%dist')
#RELEASE=1$(rpmsuffix)$(RPMDIST)
RELEASE=0
PWD=$(shell bash -c "pwd -P")
RPMTOP=$(PWD)/rpmbuild
SPEC=$(NAME).spec
TARBALL=$(NAME)-$(VERSION).tar.gz
SRPM=$(NAME)-$(VERSION)-$(RELEASE).src.rpm

help:
	@echo
	@echo "Usage: make <target> where <target> is one of"
	@echo
	@echo "clean     clean temp files from local workspace"
	@echo "doc       generate sphinx documentation and man pages"
	@echo "test      run functional/unit tests locally"
	@echo "tarball   generate tarball of p roject"
	@echo "rpm       build source codes and generate rpm file"
	@echo "srpm      generate SRPM file"
	@echo "all       clean test doc rpm"
	@echo "flake8    check Python style based on flake8"
	@echo "egg       build python egg to send to pypi"
	@echo "       -------- devOps ---------       "
	@echo "build     start build in copr"
	@echo "pypi      upload egg to pypi"
	@echo "testpypi  upload egg to pypi"
	@echo "docker    build docker image"
	@echo

all: clean test doc rpm

prep:
	#rpmdev-setuptree into project folder
	@mkdir -p rpmbuild/{BUILD,BUIDLROOT,RPMS,SOURCES,SPECS,SRPMS}

set-version:
	@echo $(VERSION)-$(RELEASE) > $(RPMTOP)/SOURCES/version.txt
	@cp $(RPMTOP)/SOURCES/version.txt $(RPMTOP)/BUILD/version.txt

clean:
	$(RM) $(NAME)*.tar.gz $(SPEC)
	$(RM) -r rpmbuild
	@find -name '*.py[co]' -delete
	make clean -C docs/
	rm -rf docs/build build dist janitor.egg-info janitor_osp.egg-info janitor_eduardocerqueira.egg-info

doc: prep set-version
	make -C docs/ html
	make -C docs/ man
	cp docs/build/man/janitor.1 janitor.1  

spec: $(SPEC).in prep doc
	sed \
		-e 's/@RPM_VERSION@/$(VERSION)/g' \
		-e 's/@RPM_RELEASE@/$(RELEASE)/g' \
		< $(SPEC).in \
		> $(RPMTOP)/SPECS/$(SPEC)

tarball: spec
	git ls-files | tar --transform='s|^|$(NAME)/|' \
	--files-from /proc/self/fd/0 \
	-czf $(RPMTOP)/SOURCES/$(TARBALL) $(RPMTOP)/SPECS/$(SPEC)

srpm: tarball
	rpmbuild --define="_topdir $(RPMTOP)" --define "_specdir $(RPMTOP)/SPECS" \
	-ts $(RPMTOP)/SOURCES/$(TARBALL)

rpm: srpm
	rpmbuild --define="_topdir $(RPMTOP)" --rebuild $(RPMTOP)/SRPMS/$(SRPM)

build: srpm
	# run build in copr project depending of your local branch.
	# you need to have a valid ~/.config/copr-fedora file to use copr-cli
	@echo "building source-code from branch $(BRANCH)"
	@echo "running build in https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/"
	@copr-cli --config /home/$(USER)/.config/copr-fedora \
	build eduardocerqueira/janitor $(RPMTOP)/SRPMS/$(SRPM) 

egg: srpm
	@echo "building egg from branch $(BRANCH)"
	python3 -m build

pypi: egg
	@echo "uploading new version to pypi"
	python3 -m twine upload dist/*

testpypi: egg
	@echo "uploading new version to test.pypi"
	python3 -m twine upload --repository testpypi dist/*

docker:
	@echo "building new docker image"
	docker build -f Dockerfile . -t ecerquei/janitor

# Unit tests
TEST_SOURCE=tests
TEST_OUTPUT=$(RPMTOP)/TESTS
TEST_UNIT_FILE=unit-tests.xml

test: prep
	@mkdir $(TEST_OUTPUT)
	nosetests --verbosity=3 -x --with-xunit --xunit-file=$(TEST_OUTPUT)/$(TEST_UNIT_FILE)	
	@echo

# Check code convention based on flake8
CHECK_DIRS=.
FLAKE8_CONFIG_DIR=tox.ini

flake8:
	flake8 $(CHECK_DIRS) --config=$(FLAKE8_CONFIG_DIR)

