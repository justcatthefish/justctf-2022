#ifndef __ACTION_H
#define __ACTION_H
#include "monster.h"

// justCTF2022 ~ Tacet

enum FightResult {
    NoFight,
    Win,
    Loss
};

FightResult fight(monster &a, monster &b);
bool create_note(std::string &note);
void make_note(std::string &paper);
monster generate_boss_monster();
monster generate_players_monster();
monster generate_queen_monster();

__attribute__((optnone, noinline))
std::string get_flag();

monster generate_random_monster_external();

#endif // __ACTION_H
