#ifndef __MONSTER_H_
#define __MONSTER_H_
#include <string>
#include <tuple>

// justCTF2022 ~ Tacet

using message_t = std::tuple<bool, std::string>;

class monster {
  public:
    using thinking_t = message_t (*)(monster const &);

    unsigned life, strength, experience = 0;
    thinking_t decision_process = nullptr;
  
    std::string name;
    std::string note = "";
    std::string kind;

    monster(unsigned const life, unsigned const strength,
      std::string const name, std::string const kind) :
      life(life), strength(strength), name(name), kind(kind) {
    }
    
    monster(unsigned const life, unsigned const strength,
      std::string const name, std::string const kind, thinking_t const decision_process) :
      life(life), strength(strength), decision_process(decision_process), name(name), kind(kind) {
    }
    
    monster(monster &&) = default;
    monster(monster const &) = default;
    monster &operator=(monster &&) = default;
    monster &operator=(monster const &) = default;

    virtual message_t is_ready_to_fight(monster const &opponent) {
      if(decision_process == nullptr)
        return {false, "Please, no!"};
      
      return decision_process(opponent);
      };

    static void print_description(monster  const &m) {
      std::cout << "name: " << m.name << std::endl;
      std::cout << "kind: " << m.kind << std::endl;
      std::cout << "life: " << m.life << std::endl;
      std::cout << "strength: " << m.strength << std::endl;
      if(m.note != "") {
        std::cout << "Your note: " << m.note << std::endl;
      }
    }
};

#endif // __MONSTER_H_
