#include <iostream>
#include <string>

// justCTF2022 ~ Tacet

void change_size_byte(std::string &s, uint8_t const new_size) {
    unsigned char* const size_ptr = (unsigned char *)&s;
    *size_ptr = new_size;
}

void foo(std::string s) {
    change_size_byte(s, 1);
    s = "New content!!!!!!!!!!!!";
    change_size_byte(s, 0);
}

int main() {
    std::string s = "This is a very, very long string! I caannot imagine how long that string is... can you?";
    for(size_t i = 0; i < 32; ++i) {
        s.push_back('?');
    }

    change_size_byte(s, 2);
    foo(s);
    change_size_byte(s, 11*2+1);
    std::cout << s << std::endl;
}
