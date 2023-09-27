PYTHON=python3
PIP=$(PYTHON) -m pip
DELIVERY_PATH=target

install:
	$(PIP) install .

install_dev:
	$(PIP) install -e .

build:
	rm -rf dist && mkdir dist  || true
	$(PYTHON) setup.py bdist_wheel -d dist/ && rm -rf build

clean:
	rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info

uninstall:
	$(PIP) uninstall -y $(shell basename $(CURDIR))

doc:
	$(PIP) install -r .requirements.docs.txt
	mkdocs build -d "${DELIVERY_PATH}/doc_html"
	@echo "README:"
	@echo "Deploy your doc by copying the content of [${DELIVERY_PATH}/doc_html] into gs://totor-deep-doc/<my_project>"
	@echo "Your doc will soon be available at http://localhost:2224/bucket/<my_project>/"
