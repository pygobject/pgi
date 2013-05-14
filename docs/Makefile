DIAS = $(wildcard images/*.dia)
PNGS = $(patsubst %.dia,%.png,$(DIAS))

all: html

.PHONY: clean html latex pdf

images/%.png: images/%.dia
	dia $< --export=$@ --filter=cairo-alpha-png

setup: $(PNGS)

html: setup
	sphinx-build -n . _html

latex: setup
	rm -rf _latex
	sphinx-build -b latex -n . _latex

_latex/pgi.pdf: latex
	$(MAKE) -C _latex

pdf: _latex/pgi.pdf

clean:
	rm -rf _html
	rm -rf _latex
