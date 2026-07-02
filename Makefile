PDF := contemporary-artists-guide-to-industrial-displays.pdf
SOURCES := contemporary-artists-guide-to-industrial-displays.md panel-pc-buying-guide.md

.PHONY: pdf deps clean

pdf: $(PDF)

$(PDF): $(SOURCES) build_pdf.py
	python3 build_pdf.py

# One-time setup. On macOS, WeasyPrint also needs pango: brew install pango
deps:
	python3 -m pip install -r requirements.txt

clean:
	rm -f $(PDF)
