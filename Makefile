VENV_DIR = .venv

install-deps: clean
	python3 -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements.txt

build-c:
	${VENV_DIR}/bin/python setup.py build_ext --inplace

build: install-deps build-c

clean:
	rm -rf tg.h tg.c togo.c* build/ ${VENV_DIR} .dist-deps dist/ *.egg-info/

dist-sdist:
	${VENV_DIR}/bin/python setup.py sdist

dist-wheel:
	${VENV_DIR}/bin/python setup.py bdist_wheel

dist-check:
	${VENV_DIR}/bin/twine check dist/*

# Upload to PyPI: requires credentials configured (e.g., in ~/.pypirc or env vars)
publish-wheel:
	${VENV_DIR}/bin/twine upload dist/*.whl

publish-sdist:
	${VENV_DIR}/bin/twine upload dist/*.tar.gz

test:
	${VENV_DIR}/bin/pytest

bench:
	${VENV_DIR}/bin/pip install shapely
	${VENV_DIR}/bin/python benchmarks/bench_shapely_vs_togo.py

.PHONY: build install-deps build-c clean test dist-check dist-sdist dist-wheel publish-wheel publish-sdist bench
