#pragma once

#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
#include <map>
#include <list>
#include <unordered_set>
#include <chrono>

#include "chall_data.hpp"

using u64 = std::uint64_t;
using u32 = std::uint32_t;
using u8 = std::uint8_t;

u64 func1(u64 a, u64 b){ //div
	u64 ret = 0;
	while(a >= b){
		a -= b;
		ret++;
	}
	return ret;
}

u64 func2(u64 a, u64 b){ //mul
	u64 res=0;
	for (int i = 0; i < b; ++i) {
		res += a;
	}
	return res;
}

u64 func3(u64 a, u64 b){ //mod
	while(a >= b){
		if(a == b) return 0;
		if(a > b) a -= b;
	}
	return a;
}

u8 func0(u64 a, u64 b, u64 c, u64 d, u64 i) {
    u64 result = func2(a, b);
    result += func2(i, 0x1337);
	result = func1(result, c);
    result ^= d;
	result = func3(result, 0x80);
    return result;
}

#ifndef NDEBUG
//#include "verify_data.hpp"
//template<typename T>
//void debug(const u32 idx, u32 part, const std::vector<T> &vals, const u64 outcome) {
//    std::cout << "[" << idx << "] " << part << ". should be: " << chall_verify[idx][part] << " is_ok? " << std::boolalpha << static_cast<bool>(outcome == chall_verify[idx][part]);
//	if(outcome != chall_verify[idx][part]){
//		std::cout << "NOPE\n";
//		std::exit(1);
//	}
//    std::cout << std::endl;
//}
#else
template<typename T>
void debug(const u32 idx, const char part, const std::vector<T> &vals, const u64 outcome) {};
#endif