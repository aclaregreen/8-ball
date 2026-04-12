CC=clang
CFLAGS=-Wall -std=c99 -pedantic
PYTHON=/usr/include/python3.12/

all: _phylib.so

clean:
	rm -f *.o *.so phylib _phylib.so phylib_wrap.c *.svg

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so -lm

phylib_wrap.c: phylib.i libphylib.so
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -fPIC -I$(PYTHON) -c phylib_wrap.c -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON) -lpython3.12 -lphylib -o _phylib.so

#export LD_LIBRARY_PATH=.