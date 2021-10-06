sdist: clean test
	python3 setup.py sdist

publish: sdist
	twine upload --repository pypi dist/*

test:
	python3 tests/uec.py

clean:
	rm -rf build/ dist/ *.egg-info/
