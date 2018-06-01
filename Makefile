.PHONY: default

help:
	@echo compile
	@echo push
	@echo debug
	@echo install 
	@echo watch

compile:
	python md_to_html.py md/*.md

push:
	$(MAKE) compile
	-git add *.html md/*.md
	-git commit *.html md/*.md -mup
	-git reset $$(git commit-tree HEAD^{tree} -m "up")
	-git push -f

debug:
	git commit-tree HEAD^{tree} -m "up"

install:
	pip install markdown

watch:
	while true; \
	do \
		inotifywait -qq -r -e modify,create md  && make compile; \
	done
