VENV_DIR = .venv
DIST_DIR = dist

install-deps: clean
	python3 -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -U pip -r requirements.txt
	${VENV_DIR}/bin/python tools/prepare_tg.py

build-wheel:
	$(VENV_DIR)/bin/python -m build --wheel

build: install-deps build-wheel

clean:
	rm -rf tg.h tg.c tgx.h tgx.c togo.c* build/ ${VENV_DIR} ${DIST_DIR}/ *.egg-info/

dist-check:
	${VENV_DIR}/bin/twine check ${DIST_DIR}/*

# Upload to PyPI: requires credentials configured (e.g., in ~/.pypirc or env vars)
publish:
	${VENV_DIR}/bin/twine upload ${DIST_DIR}/*.tar.gz

test:
	$(VENV_DIR)/bin/pytest

bench:
	${VENV_DIR}/bin/pip install shapely
	${VENV_DIR}/bin/python benchmarks/bench_shapely_vs_togo.py
	${VENV_DIR}/bin/pip uninstall -y shapely

.PHONY: install-deps build-wheel build clean test dist-check publish bench
