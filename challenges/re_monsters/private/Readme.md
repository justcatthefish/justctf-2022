### Monsters

It's kind of "next notepad task" but with console RPG elements.
At the same time, there is no PWNing.

Bug: BO, off by one

Getting flag is based on string copy optimizations in libcxx (clang++).

 There are 3 PoCs:

 Value after `\0` is copied:
```cpp
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
```

You can rea after a string (even if there is a null-terminator):
```cpp
int main () {

    std::string st[2] = {"AAAAAAAAAAAAA", "XXXXXXXXXXXXXXX"};
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
```

You can fore-copy buffer address and modify content by modifying different string:
```cpp
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
```

All that is based on Short String Optimization.