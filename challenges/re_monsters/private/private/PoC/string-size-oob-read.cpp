#include <iostream>

// justCTF2022 ~ Tacet

int main () {

    std::string st[2] = {"KASIA I BASIA", "MARIOLA I JOLA"};
    std::string &s = st[0];
    void const *const s_ptr = s.data();

    std::cout << (void *)&s << std::endl;
    std::cout << s_ptr << std::endl;

    unsigned char* const size_ptr = (unsigned char *)&s;
    std::cout << (unsigned)*size_ptr << std::endl;
    s = "AB";
    std::cout << (unsigned)*size_ptr << std::endl;
    *size_ptr = 80;
    std::cout << s << std::endl;
}
