#
# Make file for docs and test.  Docs aren't setup yet
# Most of it gets generated in nanites/client/swagger, but for some reason, a nanites.client.swagger directory
# is also created.  Contents are copied to the correct location and the dir is removed.
#
PACKAGE_NAME=ifx
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = docs/src
BUILDDIR      = docs/build

PRODIMAGE     = harvardinformatics/ifx:latest
PRODBUILDARGS = --ssh default

DEVIMAGE      = ifx
DEVBUILDARGS  = --ssh default
DEVFILE       = Dockerfile

DOCKERCOMPOSEFILE = docker-compose.yml
DOCKERCOMPOSEARGS =


help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: test Makefile prod build
prod: clean
	./set-version.sh
	docker build -t $(PRODIMAGE) $(PRODBUILDARGS) --no-cache .
	docker push $(PRODIMAGE)
build:
	docker build -t $(DEVIMAGE) -f $(DEVFILE) $(DEVBUILDARGS) .
up: buid
	docker-compose -f $(DOCKERCOMPOSEFILE) $(DOCKERCOMPOSEARGS) up
down:
	docker-compose -f $(DOCKERCOMPOSEFILE) down

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXAPIDOC) -e -M --force -o "$(SOURCEDIR)" nanites
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
