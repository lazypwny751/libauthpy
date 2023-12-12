LIBNAME := libauth

install:
	pip3 install .

uninstall:
	pip3 uninstall $(LIBNAME)

reinstall: uninstall install

.PHONY: install uninstall reinstall
