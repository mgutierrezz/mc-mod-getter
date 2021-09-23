repo=`grep -m 1 __title__ ./mc_mod_getter/__version__.py | grep -o "=.*" | cut -d\   -f2 | cut -d "'" -f2`
version=`grep -m 1 __version__ ./mc_mod_getter/__version__.py | grep -o "=.*" | cut -d\   -f2 | cut -d "'" -f2`
pypi_url=https://pypi.org/project/mc-mod-getter/

.PHONY: intro
intro:
	@echo "$(repo) $(version)"


.PHONY: clean
clean:
	-rm -rf ./build ./dist ./__pycache__/ ./$(repo)/__pycache__/
	-rm -rf ./$(repo)/$(repo).egg-info ./.eggs ./$(repo).egg-info
	-rm -f *.pyc *.pyo *.pyd *\$$py.class *.spec
	-find . -name "*.pyc" -exec rm -f {} \;


.PHONY: build
build:
	@python3 -m pip install pyinstaller 
	@python3 -m PyInstaller --onefile mc_mod_getter/__main__.py


.PHONY: install
install:
	@python3 -m pip install .


.PHONY: uninstall
uninstall:
	echo "python3 -m pip uninstall $(repo)==$(version) -y"
	@python3 -m pip uninstall $(repo)==$(version) -y

