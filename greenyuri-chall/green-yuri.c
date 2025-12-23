// gcc -no-pie -o green-yuri green-yuri.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_DAYS 0x80

typedef struct {
	char album_name[16];
	char artist_name[16];
	short song_count;
	bool completed;
} Album;

double paychecks[MAX_DAYS] = {};
int days = -1;

void menu(void) {
	puts("~-~-~-~-~-");
	puts("(1) write your album");
	puts("(2) put in another shift at the record shop");
	puts("(3) send her the completed album");
	puts("~-~-~-~-~-");
	puts("");
	printf("what are we doing today? > ");
}

void win(void) {
	puts("you've finally finished the album!");
	system("cat flag.txt");
	exit(0);
	return;
}

int main(void) {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	// preamble
	puts("you are mitsuki koga, aspiring rock musician in a new relationship with your beloved aya oosawa.");
	puts("your first album is going to be dedicated to her.");
	puts("but a fierce bout of writer's block has prevented you from successfully finishing the album!");
	puts("to win this challenge, you must complete the album and present it to her.");
	puts("so: what will we do today?");
	while (1) {
		char c;
		days++;
		menu();
		char choice = getc(stdin);
		getchar(); // exhaust newline
		switch (choice) {
			case '1':
				puts("no matter how hard you try, you just can't seem to finish it...");
				break;
			case '2':
				printf("how much money did you make today? > ");
				if (scanf("%lf", &paychecks[days]) == 1) {
					while ((c = getchar()) != '\n' && c != EOF);
					printf("you made %lf dollars today!\n", paychecks[days]);
				} else puts("invalid input...");
				break;
			case '3':
				unsigned long long addr;
				printf("alright! finally. where's your album stored at? > ");
				scanf("%llx", &addr);
				while ((c = getchar()) != '\n' && c != EOF);
				Album *album = (Album *) addr;
				if (
					!strncmp(album->album_name, "me to her", 16) &&
					!strncmp(album->artist_name, "mitsuki koga", 16) &&
					album->song_count==10 &&
					album->completed
				) win();
				puts("hmmm.. seems like the album isn't quite finished yet...");
				break;	
			case 'q':
			default:
				goto fin;
		}

	}	

	fin:
		puts("maybe you'll be able to finish it some other time...");
		exit(0);

}
