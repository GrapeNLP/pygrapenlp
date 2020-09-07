

PYVER := 3.6

PYNAME := $(shell echo $(PYVER) | tr -d .)

LIB := src/pygrapenlp/_pygrapenlp.cpython-$(PYNAME)m-x86_64-linux-gnu.so


# ----------------------------------------------------------------------------

.PHONY: build

all: build

dbg: build-dbg

build clean:
	python$(PYVER) setup.py $@

build-dbg:
	GRAPENLP_DEBUG=1 \
	GRAPENLP_DIR=../grapenlp-core python$(PYVER)-dbg setup.py build

clean-dbg:
	GRAPENLP_DEBUG=1 \
	GRAPENLP_DIR=../grapenlp-core python$(PYVER)-dbg setup.py clean



clean_all: clean
	rm $(LIB)
	python$(PYVER) setup.py clean
