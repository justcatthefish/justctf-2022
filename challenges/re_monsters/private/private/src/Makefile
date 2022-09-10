monsters: action.o *.cpp *.h
	clang++ -fPIE -O3 -g3 -Wall -Wextra -pedantic  -stdlib=libc++ -std=c++20 action.o main.cpp -o monsters

action.o: action.cpp action.h
	clang++ -fPIE -O3 -g0 -Wall -Wextra -pedantic -stdlib=libc++ -std=c++20 -c action.cpp

clean:
	rm monsters action.o
