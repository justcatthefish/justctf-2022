#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char *user="admin";
const char *pass="admin1";

void read_bytes(char *ptr, int n) {
  for (int i=0; i!=n; i++, ptr++) {
    read(0, ptr, 1);
    if (*ptr == '\n' || *ptr=='\0' || *ptr=='\x1b' || *ptr=='\xa8' || *ptr=='\x13') break;
  }
}

int auth() {
	char u[16],p[16];

	puts("Turrbomower 65000FU\n");
	printf("login: ");
	read_bytes(u,15);
	printf("password: ");
	read_bytes(p,15);

	if(strncmp(u,user,strlen(user)) == 0 && strncmp(p,pass,strlen(pass)) == 0) {
		return 1;
	} else {
		return 0;
	}
}

void cli() {
        char str[100];
        char buf[256];
	int x=0;

        while(1){
                printf("> ");
                read_bytes(buf,256);

                if(strncmp(buf,"exit",4) == 0){
			return;
                }
                else if(strncmp(buf,"echo",4) == 0 && x==1){
                        strncpy(str,buf+5,strlen(buf));
                        printf(str);
                }
                else if(strncmp(buf,"status",6) == 0){
			system("uptime");
                }
                else if(strncmp(buf,"mode",4) == 0){
                	if(strncmp(buf+5,"advanced",8) == 0) {
				x=1;
                        	puts("advanced mode enabled\n");
                        } else {
                        	puts("unknown mode");
                        }
                }
                else {
			if(!x) {
                        	printf("status - prints device status\nexit - end cli session\n");
			} else {
				printf("status - prints device status\necho <string> - prints <string>\nexit - end cli session\n");
			}
                }
		memset(buf,0,256);
        }
}

int main() {
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);

	if(auth()) {
		cli();
	} else {
		puts("Sorry.");
	}

	return 0;
}