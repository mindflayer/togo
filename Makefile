VENV_DIR = .venv

build: clean
	python3 -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements.txt
	${VENV_DIR}/bin/python setup.py build_ext --inplace

clean:
	rm -rf tg.h tg.c togo.c* build/ ${VENV_DIR} .dist-deps dist/ *.egg-info/

# Build sdist and wheel into dist/
.dist-deps:
	${VENV_DIR}/bin/pip install wheel twine
	touch .dist-deps

dist: build .dist-deps
	${VENV_DIR}/bin/python setup.py sdist bdist_wheel
	${VENV_DIR}/bin/twine check dist/*

# Upload to PyPI: requires credentials configured (e.g., in ~/.pypirc or env vars)
upload: dist
	${VENV_DIR}/bin/twine upload dist/*

test: build
	pytest

bench: build
	${VENV_DIR}/bin/pip install shapely
	${VENV_DIR}/bin/python benchmarks/bench_shapely_vs_togo.py

.PHONY: build clean test dist upload bench
