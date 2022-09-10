#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int get_int(){
	char input[16];

	read(0, input, 16);
	return strtoul(input, 0, 0);
}

int main(int argc, char **argv) {
	size_t idx,n,i=0;
	char *notes[10] = {NULL};
	int nmax;

	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);

	puts("\n=== Welcome to the Notepad ===\n");
	printf("How many notes you plan to use? (0-10): ");
	nmax = get_int();
	if(nmax > 10) {
		puts("Bye");
		exit(0);
	}

	while(1) {
		puts("1. add note");
		puts("2. delete note");
		printf("3. view notes (%ld/%d)\n",i,nmax);
		puts("4. exit");
		printf("> ");
		idx = get_int();

		switch(idx){
			case 1:
				if(i < nmax) {
					printf("size: ");
					n = get_int();
					if ( n > 256 || n < 1 ) {
						puts("Allowed note size: 1 - 256 bytes\n");
	        } else {
						notes[i] = malloc(n);
						if(notes[i]) {
							printf("content: ");
							read(0,notes[i],n);
							printf("note %ld added!\n",i);
						}
						i++;
					}
				}
				else {
					puts("Number of notes exceeded.\n");
				}
				break;

			case 2:
				printf("note id: ");
				n = get_int();
				if( n <= i && notes[n] ) {
					//notes[n] = NULL;
					free(notes[n]);
					printf("note %ld deleted!\n",n);
				}
				else {
					puts("No such note.");
				}
				break;

			case 3:
				printf("note id: ");
				n = get_int();
				if( notes[n] && n < i ) {
					printf("%s\n",notes[n]);
				} else {
					puts("No such note.\n");
				}
				break;

			case 4:
				puts("Thank you for calling. Bye.");
				exit(0);
				break;

			default:
				puts("huh?");
				break;
		}
	}
	return 0;
}