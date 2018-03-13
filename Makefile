
ARCHIVE = sugar
all:
	find . -name \*.pyc -o -iname \*.pyo -delete
	zip -r $(ARCHIVE) * --exclude Makefile

clean:
	rm -f $(ARCHIVE).zip

