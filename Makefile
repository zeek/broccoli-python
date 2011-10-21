# Makefile not needed to build module. Use "python setup.py install" instead.

CLEAN=build broccoli_intern_wrap.c broccoli_intern.py README.html *.pyc build

all : broccoli_intern_wrap.c

broccoli_intern_wrap.c :  broccoli_intern.i
	swig -python -I../../src -o broccoli_intern_wrap.c broccoli_intern.i

clean:
	rm -rf $(CLEAN)

docs: README
	rst2html.py README >README.html

dist:
	rm -rf build/*.tar.gz
	python setup.py sdist -d build
	@printf "Package: "; echo build/*.tar.gz

distclean:
	rm -rf build/
