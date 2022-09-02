DESTDIR=/
build:
	: please run Make install
install:
	mkdir -p $(DESTDIR)/usr/share/osk || true
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	mkdir -p $(DESTDIR)/usr/share/icons/ || true
	install src/*.py $(DESTDIR)/usr/share/osk/
	install data/osk.desktop $(DESTDIR)/usr/share/applications/
	install data/icon.svg $(DESTDIR)/usr/share/icons/osk.svg
