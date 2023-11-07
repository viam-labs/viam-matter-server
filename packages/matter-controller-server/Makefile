build: clean-dist
	python -m build

bundle: build
	tar -czf module.tar.gz *.sh src dist pyproject.toml .env README.md

upload:
	viam module upload --version $(version) --platform linux/arm64 module.tar.gz
	viam module upload --version $(version) --platform linux/amd64 module.tar.gz

clean-dist:
	rm -rf dist

clean: clean-dist
	rm module.tar.gz

publish: bundle upload clean
