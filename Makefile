PDF := contemporary-artists-guide-to-industrial-displays.pdf
SOURCES := contemporary-artists-guide-to-industrial-displays.md panel-pc-buying-guide.md

.PHONY: pdf
pdf:
	pandoc $(SOURCES) \
		--from=gfm \
		--pdf-engine=xelatex \
		--variable=mainfont:"Arial Unicode MS" \
		--toc \
		--number-sections \
		--metadata title="The Contemporary Artist's Guide to Industrial Displays" \
		--output $(PDF)
