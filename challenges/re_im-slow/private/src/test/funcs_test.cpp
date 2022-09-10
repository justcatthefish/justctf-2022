#include "gtest/gtest.h"
#include "funcs.hpp"

TEST(SortTests, sort_small) {
    std::vector<int> vec{6,4,1,2,8,9};
    auto sorted = c_func(vec, std::less<>());
    ASSERT_TRUE(std::is_sorted(sorted.begin(), sorted.end()));
}

TEST(SortTests, sort_empty) {
    std::vector<int> vec{};
	auto sorted = c_func(vec, std::less<>());
	ASSERT_TRUE(std::is_sorted(sorted.begin(), sorted.end()));
}

TEST(SortTests, sort_sorted) {
    std::vector<int> vec{1,2,3,4};
	auto sorted = c_func(vec, std::less<>());
	ASSERT_TRUE(std::is_sorted(sorted.begin(), sorted.end()));
}

TEST(SortTests, sort_reversed) {
    std::vector<int> vec{1,2,3,4};
	auto sorted = c_func(vec, std::less<>());
	ASSERT_TRUE(std::is_sorted(sorted.begin(), sorted.end()));
}

TEST(IsEvenTests, is_ok){
    ASSERT_TRUE(ise(12));
    ASSERT_FALSE(ise(13));
}

TEST(MyGet, get_min){
    std::vector<int> vec{6,8,3,2,9,3,1,5};
    auto v = ab_func(vec, std::less<>());
    ASSERT_EQ(v, *std::min_element(vec.begin(), vec.end()));
}

TEST(MyGet, get_min_single){
    std::vector<int> vec{6};
    auto v = ab_func(vec, std::less<>());
    ASSERT_EQ(v, *std::min_element(vec.begin(), vec.end()));
}

TEST(MyGet, get_max){
    std::vector<int> vec{6,8,3,2,9,3,1,5};
    auto v = ab_func(vec, std::greater<>());
    ASSERT_EQ(v, *std::max_element(vec.begin(), vec.end()));
}

TEST(MyGet, get_max_duplicates){
    std::vector<int> vec{1,1,1,1,1,1,1};
    auto v = ab_func(vec, std::greater<>());
    ASSERT_EQ(v, *std::max_element(vec.begin(), vec.end()));
}

TEST(MyGet, get_max_duplicates2){
    std::vector<int> vec{1,1,1,1,1,1,2,1};
    auto v = ab_func(vec, std::greater<>());
    ASSERT_EQ(v, *std::max_element(vec.begin(), vec.end()));
}

TEST(MyGet, get_max_single){
    std::vector<int> vec{6};
    auto v = ab_func(vec, std::greater<>());
    ASSERT_EQ(v, *std::max_element(vec.begin(), vec.end()));
}

TEST(d_func_test, return_proper_value) {
	std::vector<int> vec {2, 10, 11, 12, 13, 14, 15, 16, 17, 18};
	auto ret = d_func(vec);
	ASSERT_EQ(ret, 2);
}
