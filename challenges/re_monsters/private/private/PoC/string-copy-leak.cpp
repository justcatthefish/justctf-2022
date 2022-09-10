#include <iostream>
#include <string>

// justCTF2022 ~ Tacet

void foo(std::string b) {
    b[1] = 'c';
    std::cout << &b[0] << std::endl;
}

int main() {
    std::string s(10, 'a');
    std::cout << s << std::endl;
    s = "K";
    foo(s);
    std::cout << s << std::endl;
}
