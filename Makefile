# a '-' before a shell command causes make to ignore its exit code (errors)

install:
	python setup.py install

uninstall:
	yes | pip uninstall discoursekernels

clean:
	find . -name '*.pyc' -delete
	rm -rf build dist discoursekernels.egg-info __pycache__

reinstall: clean uninstall install

lint:
	flake8 src

