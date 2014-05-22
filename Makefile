VERSION=1.0.3
NAME=njs2rpm
RPMTOPDIR=`pwd`/rpmbuild

all: clean dist

dist:
	rm -f $(NAME)-$(VERSION).tar.gz;\
	rm -rf $(NAME)-$(VERSION);\
	mkdir $(NAME)-$(VERSION); \
	tar -c --exclude ".svn" --exclude "$(NAME)-$(VERSION)" --exclude "rpmbuild" . | tar -x -C $(NAME)-$(VERSION);\
	tar -czvf $(NAME)-$(VERSION).tar.gz  $(NAME)-$(VERSION);\
	rm -rf $(NAME)-$(VERSION)
clean:
	rm -rf *.tar.gz $(RPMTOPDIR) RPMS
rpm: clean dist
	mkdir -p $(RPMTOPDIR)/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}; \
	cp $(NAME).spec $(RPMTOPDIR)/SPECS;\
	cp $(NAME)-$(VERSION).tar.gz $(RPMTOPDIR)/SOURCES;\
	rpmbuild  --define "_topdir $(RPMTOPDIR)" -bb $(RPMTOPDIR)/SPECS/$(NAME).spec
