#pragma once

#include "common.hpp"

template<typename T, typename F>
std::vector<T> c_func(std::vector<T> &vals, F comparator) {
	std::sort(vals.begin(), vals.end(), comparator);
	return vals;
}

template<typename T>
bool ise(T v) {
	return v % 2 == 0;
}

template<typename T, typename F>
T ab_func(const std::vector<T> &vals, F comparator) {
	return *std::min_element(vals.begin(), vals.end(), comparator);
}

bool d_func_worker(int number) {
	if (number < 2) return false;
	if (number == 2) return true;
	if (number % 2 == 0) return false;
	for (int i = 3; (i * i) <= number; i += 2) {
		if (number % i == 0) return false;
	}
	return true;
}

template<typename T>
T d_func(const std::vector<T> &vals) {
	std::vector<T> candidates;
	std::copy_if(vals.begin(), vals.end(), std::back_inserter(candidates), [](T v) { return v < 10000 && v > 1000 && d_func_worker(v); });

	std::unordered_map<T, u32> counts;
	for (const auto s: candidates) {
		counts[s] = 0;
	}

	for (const auto v: vals) {
		for (const auto s: candidates) {
			if (v % s == 0) {
				counts[s]++;
			}
		}
	}

	auto d = std::max_element(counts.begin(), counts.end(),
							  [](const typename decltype(counts)::value_type &p1,
								 const typename decltype(counts)::value_type &p2) {
								  return p1.second < p2.second;
							  });

	return d->first;
}

template<typename T>
std::vector<T> g(const std::vector<std::pair<T, T>> &to_extract) {
	std::vector<T> out;
	out.reserve(to_extract.size() * 100);
	for (const auto &[s, e]: to_extract) {
		for (int i = s; i <= e; ++i) {
			out.push_back(i);
		}
	}

	return out;
}

void print_flag() {
	u32 idx = 0;
	for (const auto &char_data: atad) {
		const auto &a_data = char_data[0];
		const auto &b_data = char_data[1];
		const auto &c_data = char_data[2];
		const auto &d_data = char_data[3];

		const auto a_vals = g<u32>(a_data);
		const auto a = ab_func(a_vals, std::less<>());

		const auto b_vals = g<u32>(b_data);
		const auto b = ab_func(b_vals, std::greater<>());

		auto c_vals = g<u32>(c_data);
		c_func(c_vals, std::less<>());
		const auto c = c_vals.at(c_vals.size() / 2);

		const auto d_vals = g<u32>(d_data);
		const auto d = d_func(d_vals);

		const auto flag_char = func0(a, b, c, d, idx);

		idx += 1;
		std::cout << flag_char << std::flush;
	}
}
