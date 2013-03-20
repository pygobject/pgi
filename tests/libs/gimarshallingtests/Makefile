FLAGS=`pkg-config --cflags glib-2.0 gio-2.0`
LIBS=`pkg-config --libs glib-2.0 gio-2.0`

NSVERSION=1.0
NAMESPACE=GIMarshallingTests
GI_NAME=$(NAMESPACE)-$(NSVERSION)
NAME=gimarshallingtests

all: lib$(NAME).la lib$(NAME).so $(GI_NAME).typelib

$(NAME).o: $(NAME).c $(NAME).h
	libtool --mode=compile gcc -g $(FLAGS) -c -Wall $(NAME).c

$(NAME).lo: $(NAME).o

lib$(NAME).la: $(NAME).lo
	libtool --mode=link gcc $(LIBS) -o $@ $(NAME).lo

lib$(NAME).so: $(NAME).lo
	libtool --mode=link gcc --shared $(LIBS) -o $@ $(NAME).lo

$(GI_NAME).gir: lib$(NAME).la $(NAME).c $(NAME).h
	g-ir-scanner \
	--nsversion=$(NSVERSION) --namespace=$(NAMESPACE) \
	--warn-all \
	--symbol-prefix=gi_marshalling_tests \
	--include=Gio-2.0 \
	--library=lib$(NAME).la \
	--output=$@ $(NAME).c $(NAME).h

$(GI_NAME).typelib: $(GI_NAME).gir
	g-ir-compiler -l lib$(NAME).so $(GI_NAME).gir > $@

.PHONY: clean

clean:
	rm -rf .libs
	rm -f $(NAME).o lib$(NAME).so lib$(NAME).la $(NAME).lo \
	$(GI_NAME).gir $(GI_NAME).typelib \

