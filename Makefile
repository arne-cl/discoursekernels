# a '-' before a shell command causes make to ignore its exit code (errors)

install:
	python setup.py install

uninstall:
	yes | pip uninstall discoursekernels

clean:
	find . -name '*.pyc' -delete
	rm -rf build dist src/discoursekernels.egg-info

reinstall: clean uninstall install

lint:
	flake8 src

