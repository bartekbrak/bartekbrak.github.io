.PHONY: default

help:
	@echo compile
	@echo install
	@echo watch

compile:
	find md -name \*.md | xargs md_to_html.py
	git add *.html
	find md -name \*.md | xargs git add

install:
	pip install markdown

watch:
	while true; \
	do \
		inotifywait -qq -r -e modify,create md  && make compile; \
	done
