#ifndef STORIES_H
#define STORIES_H
#include <iostream>
#include <deque>

#include "options.hpp"
#include "action.h"
#include "trainer.h"
#include "monster.h"

// justCTF2022 ~ Tacet

options_t const main_menu = {
    {BarStory, "meet another trainer in a bar"},
    {LookAtMonster, "check how strong the monster you have"},
    {BBVisit, "go and meet the worst enemy"},
    {DreamingStart, "start dreaming about monsters"},
    {Quit, "resign"}
    };

// Very start

std::deque<trainer> random_trainers;
uint32_t random_trainer_id = 0;

trainer player(generate_players_monster());
trainer boss(generate_boss_monster());
trainer queen(generate_queen_monster());
options_t start_story() {
    std::cout << "Hey, you! No time to explain!" <<std::endl;
    std::cout << "Take that monster and defeat Big Bad Monster Trainer!" << std::endl;

    for(int i = 0; i < 1337; ++i) {
        random_trainers.emplace_back(generate_random_monster_external());
    }
    boss.warrior.kind = "VeryGoodKind";
    return { {MenuOne, "take the monster and go to the city" } };
}

//

options_t menu_1() {
    static uint32_t i = 0;
    i += 1;
    switch (i % 8)
    {
    case 0:
        std::cout << "It's a little bit cold in the city." << std::endl;
        break;

    case 3:
        std::cout << "It's a very sunny day." << std::endl;
        break;
    case 5:
        std::cout << "It's a warm night." << std::endl;
        break;
    case 7:
        std::cout << "It's so rainy!" << std::endl;
        std::cout << "You hide under an old building." << std::endl;
        break;
    default:
        std::cout << "It's a typical day in the city." << std::endl;
        break;
    }
    

    return main_menu;
}

options_t look_at_monster() {
    std::cout << "It's a very big, strong and calm monster." << std::endl << std::endl;
    monster::print_description(player.warrior);

    return main_menu;
}

// BAR

options_t const bar_options = { {BarRemember, "remember the monster your companion owns"},
    {BarFight, "offer a sparing to your companion"},
    {BarStory, "talk a little bit and go to a different part of the bar"},
    {BarPeek, "look at your companion's monster"},
    {BarNote, "make a note about the monster"},
    {MenuOne, "go out of the bar"}    
};

options_t bar_story() {
    random_trainer_id += 1;
    if(random_trainer_id == random_trainers.size()) {
        random_trainer_id = 0;
    }

    switch (random_trainer_id%8)
    {
    case 1:
        std::cout << "There is a monster fight in the middle of the bar." << std::endl;
        break;
    case 3:
        std::cout << "There is nothing interesting in the bar at the moment." << std::endl;
        break;
    case 5:
        std::cout <<"The queue is very long... but you are ready to wait." << std::endl;
    default:
        std::cout << "The bar is very loud." << std::endl;
    }

    switch(random_trainer_id%3) {
        case 1:
            std::cout << "When drinking pure water, someone stands next to you and starts a conversation." << std::endl;
            break;
        case 2:
            std::cout << "While waiting in a queue, another trainer in a black t-shirt comes to talk with you." << std::endl;
            break;
        default:
            std::cout << "When you sit next to the window, an interesting trainer joins you." << std::endl;
            break;
    }

    return bar_options;
}

options_t bar_peek() {
    std::cout << "It's a very lovely monster!" << std::endl;
    monster::print_description(random_trainers[random_trainer_id].warrior);

    return bar_options;
}

options_t bar_remember() {
    std::cout << "It's in your mind! You can dream about that monster whenever you want. :)" << std::endl;
    player.dream = random_trainers[random_trainer_id].warrior;

    return { {BarStory, "say sorry and go to another part of the bar"}, {BarFight, "suggest a big fight"}, {MenuOne, "finish drinking water and go out"}};
}

options_t bar_fight() {
    static uint32_t i = 0;
    i += 1;
    switch(i%10) {
        case 4:
            {
                std::cout << "Your companion is surprised but agrees." << std::endl;
                
                fight(player.warrior, random_trainers[random_trainer_id].warrior);
                break;
            }
        default:
            std::cout << "There is no wish for a sparing. Your companion is not happy and goes home." << std::endl;
            return { {BarStory, "go looking for someone else for sparing"}, {MenuOne, "accept that no one wants to fight and leave"}};
    }
    return {{MenuOne, "sleep in a hotel and then go back to the city"}, {Quit, "call it a day"}};
}

options_t bar_note() {
    std::cout << "It's a smart move to make a note for later." << std::endl;

    make_note(random_trainers[random_trainer_id].warrior.note);

    return { {BarStory, "say sorry and go to another part of the bar"}, {BarFight, "suggest a big fight"}, {MenuOne, "finish drinking water and go out"}};
}

// Dreaming

options_t const dreaming_options = {
    {MenuOne, "end this beautiful dream"},
    {DreamingVisualize, "describe your imagination"},
    {DreamingName, "change the name of the imaginary monster"},
    {DreamingLife, "change the life of the imaginary monster"},
    {DreamingStrength, "change how powerful the imaginary monster is"},
    {DreamingKind, "change the type of the monster"},
    {DreamingNote, "make a note for later"}
};
options_t dreaming_start() {
    std::cout << "It is good to dream." << std::endl;
    std::cout << "You can create a monster you truly desire." << std::endl;

    return dreaming_options;
}

options_t dreaming_visualize() {
    std::cout << "That's how your imaginary monster looks like: " << std::endl;
    monster::print_description(player.dream);

    return dreaming_options;
}


options_t dreaming_name() {
    std::cout << "New name: " << std::flush;
    std::cin >> player.dream.name;

    return dreaming_options;
}


options_t dreaming_life() {
    std::cout << "New life: " << std::flush;
    std::cin >> player.dream.life;

    return dreaming_options;
}


options_t dreaming_strength() {
    std::cout << "How strong your dream monster should be? " << std::flush;
    std::cin >> player.dream.strength;

    return dreaming_options;
}


options_t dreaming_kind() {
    std::cout << "What kind of monster is that?" << std::endl << "Kind: " << std::flush;
    std::cin >> player.dream.kind;
    std::cout << "Now the kind is: ^" << player.dream.kind << "$" << std::endl;

    return dreaming_options;
}

options_t dreaming_note() {
    std::cout << "Do you want to make a note? That's smart!" << std::endl;
    std::cout << "You can make a note not to forget anything." << std::endl;
    make_note(player.dream.note);

    return {
        {MenuOne, "go back to city, you already have a note for later"}, 
        {DreamingStart, "leaving so beautiful dream is too hard for now"},
        {Quit, "the story is over"}
    };
}
// Bad

options_t const bb_options = {
    {MenuOne, "go back to the city center"},
    {BBPeek, "peek at the monster"},
    {BBRemember, "remember how the monster looks like for later"},
    {BBFight, "start the fight"},
    {BBNote, "create a note about the monster you want to fight"}
};

options_t bb_visit() {
    std::cout << "The alley is dark." << std::endl;
    std::cout << "A trainer sitting next to an old building greets you kindly." << std::endl;
    std::cout << "It's the one..." << std::endl;

    return bb_options;
}

options_t bb_peek() {
    std::cout << "Looks like a monster..." << std::endl;
    monster::print_description(boss.warrior);

    return bb_options;
}

options_t bb_remembeer() {
    std::cout << "You don't want to fight now? You will have time to prepare later..." << std::endl;
    player.dream = boss.warrior;

    return bb_options;
}

options_t bb_fight() {
    std::cout << "Do you think that you are ready?" << std::endl;
    FightResult const result = fight(player.warrior, boss.warrior);
    if(result == Win) {
        std::cout << "You did it! You really did! That's the end of the story." << std::endl;
        std::cout << "There is one more in front of you. This time you will play as someone with access to queen's palace." << std::endl;
        return { {QueenVisit, "start next story"} };
    }
    if(result == Loss) {
        return { {Quit, "this is a very sad end of the story"} };
    }
    if(result == NoFight) {
        return {
            {BarStory, "go, sit and think why monsters do not want to fight, but you do"},
            {Quit, "admit mistake"}
        };
    }
    throw std::runtime_error("Incorrect flow!");
}

options_t bb_note() {
    std::cout << "The note will be safe here... you won't forget it." << std::endl;
    make_note(boss.warrior.note);

    return bb_options;
}

// Queen

options_t queen_options = {
    {QueenPeek, "play with Queen's pet"},
    {QueenTalk, "talk with the Queen"},
    {Quit, "go home"}
};

options_t queen_visit() {
    queen.name = "Tat";
    queen.secret = get_flag();
    if(queen.secret.size() != 21) {
        throw std::runtime_error("Incorrect length!");
    }

    std::cout << "The queen is very busy, but she lets you in." << std::endl;

    return queen_options;
}

options_t queen_peek() {
    std::cout << "She has so sweet pet! :)" << std::endl;
    monster::print_description(queen.warrior);

    return queen_options;
}


options_t queen_talk() {
    std::cout << "You look at her and see a real queen." << std::endl;
    std::cout << "When she talks with you, you can feel how smart she is." << std::endl;
    std::cout << std::endl << "You try to learn more about her and that's what you see:" << std::endl;
    queen.print_description();

    std::cout << "Queen is very busy and has to go, but you can stay for a while and look at her pet." << std::endl;

    queen_options.erase(QueenTalk);
    queen_options[QueenNote] = "make a note about the pet";
    return queen_options;
}


options_t queen_note() {
    queen.secret = "C3N50RE";
    std::cout << "Queen destroyed the flag when she was leaving." << std::endl;
    make_note(queen.warrior.note);
    queen.secret = "X";

    std::cout << "There is no flag, anymore..." << std::endl;

    return queen_options;
}

#endif // STORIES_H
