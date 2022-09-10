#ifndef __TRAINER_H
#define __TRAINER_H

#include <string>
#include "monster.h"

// justCTF2022 ~ Tacet

monster const default_monster(1000, 1000000000, "Everyones dream", "Master one");

class trainer {
public:
    std::string name;
    monster dream = default_monster;
    monster warrior;
    std::string secret;

    trainer(monster warrior) : warrior(warrior) {
    }

    void peek(trainer const &npc) {
        dream = npc.warrior;
    }

    void print_description() {
        std::cout << "Name: " << name << std::endl;
        std::cout << "Has a pet: " << warrior.name << std::endl;
        std::cout << "Has flag... at the moment." << std::endl;
    }

};

#endif // __TRAINER_H
