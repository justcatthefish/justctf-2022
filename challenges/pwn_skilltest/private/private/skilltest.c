#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <stdint.h>
#include <time.h>
#include <ctype.h>

extern char __bss_start;
void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

	// Make .bss/data not writable
	uint64_t ptr = (uint64_t)&__bss_start;
	ptr = (ptr / 0x1000) * 0x1000;
	mprotect((void *)ptr, 0x1000, PROT_READ); //set PROT_WRITE for debugging
}

void cleanup() {
	uint64_t ptr = (uint64_t)&__bss_start;
	ptr = (ptr / 0x1000) * 0x1000;
	mprotect((void *)ptr, 0x1000, PROT_READ | PROT_WRITE);
	exit(0);
}

char *rtrim(char *s)
{
    char* back = s + strlen(s);
    while(isspace(*--back));
    *(back+1) = '\0';
    return s;
}

#define MAX_COLOR_LEN 0x60
#define MAX_NAME_LEN 0x20

const char bot_names[][MAX_NAME_LEN] = {
	"Amelie",
	"Bobbie",
	"Miyah",
	"Danyal",
	"Jannat",
	"Blade",
	"Hari",
	"Lizzie",
	"Aleyna",
	"Abdi"
};

const char bot_colors[5][MAX_COLOR_LEN] = {
	"Black",
	"White",
	"Pink",
	"Green",
	"Blue"
};

void print(const char *msg){
	write(STDOUT_FILENO, msg, strlen(msg));
}

typedef struct {
	const char *name;
	const char *color;
	int score;
} player_t;

ssize_t max_color_len = MAX_COLOR_LEN;
ssize_t max_name_len = MAX_NAME_LEN;

void get_username(player_t *player) {
	char name[MAX_NAME_LEN];
	char *color = malloc(max_color_len);
	memset(name, 0, max_name_len);
	memset(color, 0, max_color_len);

	while (1){
		print("Nick: ");

		// <= 0x60 needed
		if(read(STDIN_FILENO, name, max_color_len) <= 0){ // obvious bug...
			print("Invalid name, try again\n");
			continue;
		}

		print("Clan tag: ");
		if(read(STDIN_FILENO, color, max_color_len) <= 0){
			print("Invalid color, try again\n");
			continue;
		}
		break;
	}

	player->name = strdup(rtrim(name));
	player->color = rtrim(color);
	player->score = 0;
	for(ssize_t i = 0; i < strlen(player->name); i++){
		player->score += player->name[i];
		player->score %= 30;
	}

	for(ssize_t i = 0; i < strlen(player->color); i++){
		player->score += player->color[i];
		player->score %= 30;
	}
	
	print("Thanks\n");
}

void bot_setup(player_t *player) {
	#define LEN(arr) ((int) (sizeof (arr) / sizeof (arr)[0]))

	srand(time(NULL));
	int bot_name_idx = rand() % LEN(bot_names);
	int bot_color_idx = rand() % LEN(bot_colors);

	player->name = bot_names[bot_name_idx];
	player->color = bot_colors[bot_color_idx];
	player->score = 0;
	for(ssize_t i = 0; i < strlen(player->name); i++){
		player->score += player->name[i];
		player->score %= 30;
	}

	for(ssize_t i = 0; i < strlen(player->color); i++){
		player->score += player->color[i];
		player->score %= 30;
	}

	#undef LEN
}

void skilltest(player_t players[]){
	// align the stack!!
	__asm__(
		"push %rdi;"
		"sub $8, %rsp"
	);
	char buf[0x200];
	snprintf(buf, sizeof(buf), "%s [%s] vs %s [%s]\n", players[0].name, players[0].color, players[1].name, players[1].color);
	print(buf);
	if(players[1].score > players[0].score){
		print("Victory!\n");
	}else {
		print("L0ser\n");
	}
	__asm__(
		"add $8, %rsp;"
		"pop %rdi;"
	);
}

int main(){
	setup();

	print("Welcome to skilltest v12!\n");
	player_t players[2];
	memset(players, 0, sizeof(players));
	bot_setup(&players[0]);

	get_username(&players[1]);
	skilltest(players);

	cleanup();
	return 0;
}
