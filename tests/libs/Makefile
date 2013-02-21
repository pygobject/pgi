all:
	$(MAKE) -C regress
	ln -sf regress/Regress-1.0.typelib
	ln -sf regress/libregress.so
	$(MAKE) -C gimarshallingtests
	ln -sf gimarshallingtests/GIMarshallingTests-1.0.typelib
	ln -sf gimarshallingtests/libgimarshallingtests.so

.PHONY: clean

clean:
	$(MAKE) -C regress clean
	rm -f Regress-1.0.typelib libregress.so
	$(MAKE) -C gimarshallingtests clean
	rm -f GIMarshallingTests-1.0.typelib libgimarshallingtests.so
