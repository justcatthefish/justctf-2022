//#include "monster.h"
//#include "game.h"
#include <iostream>

#include "options.hpp"
#include "stories.hpp"

// justCTF2022 ~ Tacet

void print_option(uint32_t const value, std::string const &description) {
    std::cout << value << " - " << description << "." << std::endl;
}

Option menu(options_t const &options) {
    std::cout << std::endl;
    std::cout << "It's time to make important decision. What do you want to do?" << std::endl;
    if(options.size() < 2) {
        std::cout << "You don't have many options..." << std::endl;
    }
    for(auto const &[id, description] : options) {
        print_option(id, description);
    }
    std::cout << std::endl;
    std::cout << "Your decision: " << std::flush;
    int user_decision_int;
    std::cin >> user_decision_int;
    Option const user_decision = Option(user_decision_int);
    if(!options.contains(user_decision)) {
        throw std::runtime_error("Incorrect choice");
    }
    std::cout << std::endl;
    return user_decision;
}

options_t execute(Option const user_decision) {

    switch(user_decision) {
        case Quit:
            std::cout << "We hope to see you soon!" << std::endl;
            exit(0);
        case Start:
            return start_story();
        case MenuOne:
            return menu_1();
        case LookAtMonster:
            return look_at_monster();
        case BarStory:
            return bar_story();
        case BarPeek:
            return bar_peek();
        case BarRemember:
            return bar_remember();
        case BarFight:
            return bar_fight();
        case BarNote:
            return bar_note();
        case DreamingStart:
            return dreaming_start();
        case DreamingVisualize:
            return dreaming_visualize();
        case DreamingName:
            return dreaming_name();
        case DreamingLife:
            return dreaming_life();
        case DreamingStrength:
            return dreaming_strength();
        case DreamingKind:
            return dreaming_kind();
        case DreamingNote:
            return dreaming_note();
        case BBVisit:
            return bb_visit();
        case BBPeek:
            return bb_peek();
        case BBRemember:
            return bb_remembeer();
        case BBFight:
            return bb_fight();
        case BBNote:
            return bb_note();
        case QueenVisit:
            return queen_visit();
        case QueenPeek:
            return queen_peek();
        case QueenTalk:
            return queen_talk();
        case QueenNote:
            return queen_note();
        

        default:
            throw std::runtime_error("Incorrect flow.");
    }
}

int main() {
    std::cout << "RPG v. 1.0.0" << std::endl;
    options_t options = { {Start, "Start your story"} };
    while(true) {
        Option const user_decision = menu(options);
        options = execute(user_decision);
    }
}
