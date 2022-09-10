CC=gcc
CFLAGS= -fno-stack-protector -no-pie -Wl,-z,relro,-z,now -L.

skilltest: skilltest.c
	$(CC) -o $@ $(CFLAGS) $^
	patchelf --set-interpreter ./ld-linux-x86-64.so.2  $@
	patchelf --set-rpath '.' $@
	patchelf --replace-needed libc.so.6 ./libc-2.34.so $@
	strip $@

clean:
	rm -r skilltest

