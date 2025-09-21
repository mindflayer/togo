VENV_DIR = .venv

build: clean
	python3 -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements.txt
	${VENV_DIR}/bin/python setup.py build_ext --inplace

clean:
	rm -rf tg.h tg.c togo.c* build/ ${VENV_DIR}

test: build
	pytest

.PHONY: build clean test
