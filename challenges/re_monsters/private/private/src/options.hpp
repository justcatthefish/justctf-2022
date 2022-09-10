#ifndef OPTIONS_HPP
#define OPTIONS_HPP
#include <map>

// justCTF2022 ~ Tacet

enum Option : int {
    // Very start
    Start,
    // Basics
    MenuOne,
    LookAtMonster,
    Quit,
    // Bar
    BarStory,
    BarPeek,
    BarRemember,
    BarFight,
    BarNote,
    // Dreaming
    DreamingStart,
    DreamingVisualize,
    DreamingName,
    DreamingLife,
    DreamingStrength,
    DreamingKind,
    DreamingNote,
    // First big enemy
    BBVisit,
    BBPeek,
    BBRemember,
    BBFight,
    BBNote,
    // Second story start
    QueenVisit,
    QueenPeek,
    QueenTalk,
    QueenNote
};

using options_t = std::map<Option, std::string>;

#endif // OPTIONS_HPP
