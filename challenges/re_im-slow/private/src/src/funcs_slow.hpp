#pragma once

#include "common.hpp"

template<typename T, typename F>
void c_func_worker(std::vector<T> &vals, F comparator, size_t i, size_t j) {
	if (i >= j) return;

	size_t m = (i + j) / 2;
	c_func_worker(vals, comparator, i, m);
	c_func_worker(vals, comparator, m + 1, j);

	if (comparator(vals.at(j), vals.at(m))) {
		std::swap(vals.at(j), vals.at(m));
	}

	c_func_worker(vals, comparator, i, j - 1);
}

template<typename T, typename F>
std::vector<T> c_func(std::vector<T> vals, F comparator) {
	if (vals.empty()) return {};
	c_func_worker(vals, comparator, 0, vals.size() - 1);
	return vals;
}

template<typename T>
bool ise(T v) {
	std::vector<T> values;
	for (size_t i = 0; i <= v; ++i) {
		values.push_back(i % 2);
	}

	auto ones = std::count(values.begin(), values.end(), 1);
	auto zeros = std::count(values.begin(), values.end(), 0);
	return zeros > ones;
}

template<typename T, typename F>
T ab_func_worker(std::vector<T> vals, F comparator) {
	std::vector<T> leftovers;
	while (vals.size() != 1) {
		leftovers.clear();
		for (size_t i = 0; i < vals.size() && i + 1 < vals.size(); i += 2) {
			if (comparator(vals.at(i), vals.at(i + 1))) {
				leftovers.push_back(vals.at(i + 1));
			} else {
				leftovers.push_back(vals.at(i));
			}
		}
		if (!ise(vals.size())) {
			leftovers.push_back(vals.back());
		}

		vals.assign(leftovers.begin(), leftovers.end());
	}
	return leftovers.front();
}

template<typename T, typename F>
T ab_func(std::vector<T> vals, F comparator) {
	std::unordered_set<T> erased;
	std::vector<T> reduced;
	while (true) {
		reduced = vals;

		for (auto v: erased) {
			reduced.erase(std::remove(reduced.begin(), reduced.end(), v),
						  reduced.end());
		}

		if (std::equal(reduced.begin() + 1, reduced.end(), reduced.begin()) ||
			reduced.size() == 1) {
			break;
		}

		erased.insert(ab_func_worker<T, F>(reduced, comparator));
	}
	return reduced.at(0);
}

bool d_func_worker(int number) {
	if (number < 2) return false;
	if (number == 2) return true;
	if (ise(number)) return false;
	for (int i = 3; func2(i, i) <= number; i += 2) {
		if (func3(number, i) == 0) return false;
	}
	return true;
}

template<typename T>
T d_func(std::vector<T> vals) {
	std::unordered_map<T, u32> counts;
	std::unordered_map<T, bool> primes;
	for (auto s: vals) {
		counts[s] = 0;
		primes[s] = d_func_worker(s);
	}

	for (auto v: vals) {
		for (auto s: vals) {
			if (primes[s] && func3(v, s) == 0) {
				counts[s]++;
			}
		}
	}

	std::vector<T> map_values;
	std::transform(counts.begin(), counts.end(), std::back_inserter(map_values), [](typename decltype(counts)::value_type v){return v.second;});

	auto max_val = ab_func(map_values, std::greater<>());
	T max_key;
	for(auto [k, v] : counts) {
		if(v == max_val){
			max_key = k;
			break;
		}
	}

	return max_key;
}

template<typename T>
std::vector<T> g(std::vector<std::pair<T, T>> to_extract) {
	std::vector<T> out;
	for (auto [s, e]: to_extract) {
		for (int i = s; i <= e; ++i) {
			out.push_back(i);
		}
	}

	return out;
}

void print_flag() {
	u32 idx = 0;
	for (auto char_data: atad) {
		u64 a, b, c, d;
		auto a_data = char_data[0];
		auto b_data = char_data[1];
		auto c_data = char_data[2];
		auto d_data = char_data[3];

		auto a_vals = g<u32>(a_data);
		a = ab_func(a_vals, std::less<>());
//		a = chall_verify[idx][0];
//		debug(idx, 0, a_vals, a);

		auto b_vals = g<u32>(b_data);
		b = ab_func(b_vals, std::greater<>());
//		b = chall_verify[idx][1];
//		debug(idx, 1, b_vals, b);

		auto c_vals = g<u32>(c_data);
		auto c_sorted = c_func(c_vals, std::less<>());
		auto c_size = c_sorted.size();
		for (int i = 0; i < (c_size / 2); i++) {
			c_sorted.erase(c_sorted.begin());
		}
		c = c_sorted.at(0);
//		c = chall_verify[idx][2];
//		debug(idx, 2, c_vals, c);

		auto d_vals = g<u32>(d_data);
		d = d_func(d_vals);
//		d = chall_verify[idx][3];
//		debug(idx, 3, d_vals, d);

		auto flag_char = func0(a, b, c, d, idx);

		idx += 1;
		std::cout << flag_char << std::flush;
//		std::cout << std::endl;
	}
}
