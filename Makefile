VENV_DIR = .venv
DIST_DIR = dist

install-deps: clean
	python3 -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements.txt

build-c:
	LD_LIBRARY_PATH=$(PWD)/vendor/geos/lib:$$LD_LIBRARY_PATH $(VENV_DIR)/bin/python setup.py build_ext --inplace

build: install-deps build-c

clean:
	rm -rf tg.h tg.c tgx.h tgx.c togo.c* build/ ${VENV_DIR} ${DIST_DIR}/ *.egg-info/

dist-sdist:
	${VENV_DIR}/bin/python setup.py sdist

dist-wheel: install-deps
	${VENV_DIR}/bin/python -m cibuildwheel --output-dir ${DIST_DIR}

dist-check:
	${VENV_DIR}/bin/twine check ${DIST_DIR}/*

# Upload to PyPI: requires credentials configured (e.g., in ~/.pypirc or env vars)
publish:
	${VENV_DIR}/bin/twine upload ${DIST_DIR}/*.tar.gz

test:
	LD_LIBRARY_PATH=$(PWD)/vendor/geos/lib:$$LD_LIBRARY_PATH $(VENV_DIR)/bin/pytest

bench:
	${VENV_DIR}/bin/python benchmarks/bench_shapely_vs_togo.py

.PHONY: build install-cdeps install-deps build-c clean test dist-check dist-sdist dist-wheel publish bench
