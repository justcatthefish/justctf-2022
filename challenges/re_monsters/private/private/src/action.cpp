#include <iostream>
#include <vector>
#include "action.h"
#include "monster.h"


// justCTF2022 ~ Tacet

__attribute__((optnone, noinline))
std::string get_flag() {
    return "justCTF{l3aki1ng_str}";
}

static void describe_fighting_decision(bool const choice, std::string const &text){
    if(choice) {
        std::cout << "agreed to fight";
    } else {
        std::cout << "didn't agree to fight";
    }

    std::cout << " and told: " << text << std::endl;
}

FightResult fight(monster &a, monster &b) {
    auto const [pm_choice, pm_text] = a.is_ready_to_fight(b);
    std::cout << "Your monster ";
    describe_fighting_decision(pm_choice, pm_text);
    auto const [npc_choice, npc_text] = b.is_ready_to_fight(a);
    std::cout << "Opponents monster ";
    describe_fighting_decision(npc_choice, npc_text);

    if(!pm_choice || !npc_choice) {
        std::cout << std::endl << "At least one monster did not agree to fight, you have to do something else." << std::endl;
        return NoFight;
    }

    std::cout << "Oh no! Fight!" << std::endl;

    while(true) {
        if(a.life <= b.strength) {
            b.experience += a.strength;
            return Loss;
        }
        a.life -= b.strength;
        if(b.life <= a.strength) {
            a.experience += b.strength;
            return Win;
        }
        b.life -= a.strength;
    }
}


static inline void change_size_byte(std::string &s, uint8_t const new_size) {
    unsigned char* const size_ptr = (unsigned char *)&s;
    *size_ptr = new_size;
}

void make_note(std::string &paper) {
    char *const data = paper.data(); 
    size_t i = 0;
    std::cout << "Note input: " << std::flush;
    while(std::isspace(std::cin.peek())) {
        std::cin.get();
    }
    while(i < sizeof(std::string)) { //  == 24
        data[i] = std::cin.get();
        if(data[i] == '\0' || (data[i] != ' ' && std::isspace(data[i]))) {
            data[i] = '\0';
            break;
        }
        ++i;
    }
    change_size_byte(paper, 2 * i);
}
static std::string const really_bad_kind = "VeryBadKind!";
monster generate_players_monster() {
    return monster(10000, 10000, "Spiny One", "World destroyer",
        [](monster const &m) -> message_t{
            if(m.kind == really_bad_kind) {
                return {true, "Ok, I will do what has to be done."};
            }
            return {false, "I do not want to fight. I will fight only when I have to, and only with " + really_bad_kind + "and not with " + m.kind + "."};
        }
    );
}

monster generate_boss_monster() {
    return monster(300, 4,  "Flower", "Calm, sweet and caring forest dwarf! <3",
        [](monster const &) -> message_t{
            return {true, "I do not want to figt, but I do not want to make you any problems as well."};
        }
    );
}

monster generate_queen_monster() {
    return monster(1000000000, 999999999,  "Greeny", "Pet",
        [](monster const &) -> message_t{
            return {false, "I will only fight to protect my queen."};
        }
    );
}

static int my_rand(void) // RAND_MAX assumed to be 32767
{
    static int64_t next = 1337;
    next = next * 1103515245 + 12345;
    return (unsigned int)(next/65536) % 32768;
}

static std::string random_name() {
    static std::vector<std::string> names = {
        "Liam",	"Olivia",
        "Noah",	"Emma",
        "Oliver", "Charlotte",
        "Elijah", "Bella",
        "Luna",
        "Charlie",
        "Lucy",
        "Cooper",
        "Max",
        "Bailey",
        "Daisy"
    };

    return names[my_rand()%names.size()];
}

static std::string random_kind() {
    static std::vector<std::string> names = {
        "Pink Gods",
        "Hell Demons",
        "Angels",
        "Fallen Angels"
    };

    return names[my_rand()%names.size()];
}

monster generate_random_monster_external() {
    return monster((my_rand()*my_rand())%31337, my_rand()%0x1337, random_name(), random_kind() );
}
