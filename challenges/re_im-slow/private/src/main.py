import random
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path
from jinja2 import Template
from multiprocessing import Pool

from z3 import Solver, BitVecs, sat, Or, Ints, And, Not, Exists, ZeroExt, BV2Int

MAX_NUM = 1_000_000
PRIMES_UPPER_BOUND = 10_000

def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True


primes = {x for x in range(1000, PRIMES_UPPER_BOUND) if is_prime(x)}


class AbstractCollector(ABC):
    def __init__(self, keep_numbers, x, idx):
        self.fixed_val = x  # value to be picked, has to be on x_pos idx
        self.keep_numbers = keep_numbers  # number of total numbers passed to sort
        self.points = []
        self.idx = idx

    def collect(self, x):
        pass

    def get_shuffled(self):
        intervals = self.get()
        if not intervals: return None
        random.shuffle(intervals)
        return intervals

    @abstractmethod
    def get(self):
        pass

    def divide_number(self, num, div):
        return [num // div + (1 if x < num % div else 0) for x in range(div)]

    def check_if_overlaps(self, to_check, intervals):
        start, end = to_check
        return any(start in range(s, e + 1) for s, e in intervals) or any(end in range(s, e + 1) for s, e in intervals)

    def expand_intervals(self, intervals):
        test = []
        for s, e in intervals:
            test.extend(list(range(s, e + 1)))

        return sorted(test)


class XorCollector2(AbstractCollector):
    def get_counts(self, intervals):
        expanded = self.expand_intervals(intervals)
        less_than_1k = list(filter(lambda v: 1000 < v < PRIMES_UPPER_BOUND, expanded))
        less_than_1k_primes = list(filter(lambda v: v in primes, less_than_1k))
        counts = defaultdict(int)
        for v in expanded:
            for s in less_than_1k_primes:
                if v % s == 0:
                    counts[s] += 1

        # max_key = max(counts, key=counts.get)
        # max_val = counts[max_key]
        # sorted_list = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        # sorted_list = list(filter(lambda item: item[1] >= max_val and item[0] != self.fixed_val, sorted_list))
        # print(f'---- target {self.fixed_val}')
        # for k, v in sorted_list:
        #     print(f'{k} -> {v}')
        # print(f'{self.fixed_val} -> {counts[self.fixed_val]}')

        return counts

    def is_valid(self, counts):
        max_key = max(counts, key=counts.get)
        max_val = counts[max_key]
        if max_key != self.fixed_val or list(counts.values()).count(max_val) > 1:
            return False
        return True

    def check_divisors(self, interval):
        s, e = interval
        if any(x % self.fixed_val == 0 for x in range(s, e + 1)):
            return True
        return False

    def get(self, maxlvl=0):
        intervals = set()
        intervals_num = max(self.idx // 10, 3)
        first_interval_len = min(round(self.keep_numbers * (1 / (intervals_num + 2))), 20)
        numbers_left = self.keep_numbers - first_interval_len
        intervals_num -= 1

        # first one random
        first_interval_before = random.randint(0, first_interval_len - 1)
        first_interval_after = first_interval_len - first_interval_before - 1
        target_interval_start = self.fixed_val - first_interval_before
        target_interval_end = self.fixed_val + first_interval_after
        intervals.add((target_interval_start, target_interval_end))

        def get_random_interval_with_divisor(int_len):
            pick_limit = MAX_NUM // self.fixed_val
            pick_min = PRIMES_UPPER_BOUND // self.fixed_val
            picked = random.randint(pick_min, pick_limit)
            picked *= self.fixed_val
            len_before = random.randint(0, picked - 1)
            len_after = int_len - len_before - 1
            random_start = picked - len_before
            random_end = picked + len_after
            return random_start, random_end

        additional_intervals = []
        intervals_lengths = self.divide_number(numbers_left, intervals_num)
        for ilen in intervals_lengths:
            while True:
                random_interval = get_random_interval_with_divisor(ilen)
                if not self.check_divisors(random_interval): continue
                if self.check_if_overlaps(random_interval, intervals): continue
                break

            intervals.add(random_interval)
            additional_intervals.append(random_interval)

        tries = 10
        counts = self.get_counts(intervals)
        while not self.is_valid(counts) and tries > 0:
            tries -= 1
            to_replace = additional_intervals.pop(0)
            intervals.remove(to_replace)
            s, e = to_replace
            to_replace_len = e - s + 1

            tries_fixup = 20
            while True:
                tries_fixup -= 1
                random_interval = get_random_interval_with_divisor(to_replace_len)
                if not self.check_divisors(random_interval): continue
                if self.check_if_overlaps(random_interval, intervals): continue
                break

            intervals.add(random_interval)
            additional_intervals.append(random_interval)
            counts = self.get_counts(intervals)

        if maxlvl > 30:
            print(f"{self.idx} max lvl reached")
            return None

        if tries <= 0:
            try:
                return self.get(maxlvl + 1)
            except:
                return None

        expanded = self.expand_intervals(intervals)
        assert self.is_valid(counts) is True
        assert len(expanded) == self.keep_numbers
        return list(intervals)


class SortCollector(AbstractCollector):
    def get(self):
        intervals = set()
        # [1,2,3,4,x,8,9,10]   # keep_numbers=8, target_index=4
        target_index = self.keep_numbers // 2
        numbers_before = target_index
        numbers_after = self.keep_numbers - target_index - 1
        intervals_num = max(self.idx // 10, 3)
        first_interval_len = round(self.keep_numbers * (1 / intervals_num))
        intervals_num -= 3  # make sure that one is before, one after and one contains fixed_val
        chances = [random.getrandbits(1) for _ in range(intervals_num)]
        intervals_before = 1 + chances.count(1)
        intervals_after = 1 + chances.count(0)

        first_interval_before = random.randint(0, first_interval_len - 1)
        first_interval_after = first_interval_len - first_interval_before - 1
        target_interval_start = self.fixed_val - first_interval_before
        target_interval_end = self.fixed_val + first_interval_after
        intervals.add((target_interval_start, target_interval_end))
        numbers_before -= first_interval_before
        numbers_after -= first_interval_after

        intervals_before_lengths = self.divide_number(numbers_before, intervals_before)
        intervals_after_lengths = self.divide_number(numbers_after, intervals_after)
        for ilen in intervals_before_lengths:
            success = False
            while not success:
                end = random.randint(ilen + 1, target_interval_start)
                start = end - ilen + 1
                if self.check_if_overlaps((start, end), intervals): continue

                intervals.add((start, end))
                success = True

        for ilen in intervals_after_lengths:
            success = False
            while not success:
                start = random.randint(target_interval_end + 1, MAX_NUM)
                end = start + ilen - 1
                if self.check_if_overlaps((start, end), intervals): continue

                intervals.add((start, end))
                success = True

        expanded = self.expand_intervals(intervals)
        assert expanded[target_index] == self.fixed_val
        assert len(expanded) == self.keep_numbers
        return list(intervals)


class MinCollector(AbstractCollector):
    def get(self):
        intervals = set()
        intervals_after = max(self.idx // 10, 3)
        first_interval_len = round(self.keep_numbers * (1 / intervals_after))
        intervals_after -= 1

        first_interval_after = first_interval_len - 1
        target_interval_start = self.fixed_val
        target_interval_end = self.fixed_val + first_interval_after
        intervals.add((target_interval_start, target_interval_end))
        numbers_after = self.keep_numbers - first_interval_len

        intervals_after_lengths = self.divide_number(numbers_after, intervals_after)
        for ilen in intervals_after_lengths:
            success = False
            while not success:
                start = random.randint(target_interval_end + 1, MAX_NUM)
                end = start + ilen - 1
                if self.check_if_overlaps((start, end), intervals): continue

                intervals.add((start, end))
                success = True

        expanded = self.expand_intervals(intervals)
        assert len(expanded) == self.keep_numbers
        assert expanded[0] == self.fixed_val
        return list(intervals)


class MaxCollector(AbstractCollector):
    def get(self):
        intervals = set()
        intervals_before = max(self.idx // 10, 3)
        first_interval_len = round(self.keep_numbers * (1 / intervals_before))
        intervals_before -= 1

        first_interval_before = first_interval_len - 1
        target_interval_start = self.fixed_val - first_interval_before
        target_interval_end = self.fixed_val
        intervals.add((target_interval_start, target_interval_end))
        numbers_before = self.keep_numbers - first_interval_len

        intervals_before_lengths = self.divide_number(numbers_before, intervals_before)
        for ilen in intervals_before_lengths:
            success = False
            while not success:
                end = random.randint(ilen + 1, target_interval_start)
                start = end - ilen + 1
                if self.check_if_overlaps((start, end), intervals): continue

                intervals.add((start, end))
                success = True

        expanded = self.expand_intervals(intervals)
        assert len(expanded) == self.keep_numbers
        assert expanded[-1] == self.fixed_val
        return list(intervals)


def func(a, b, c, d, i):
    result = a * b
    result += i * 0x1337
    if isinstance(c, int):
        result //= c
    else:
        result /= c
    result ^= d
    result %= 0x80
    return result


def ramper(start, inc, idx):
    if idx < 8:
        return start * (idx + 1)

    if 8 <= idx <= 24:
        return idx * 2 * inc

    if 24 < idx <= 50:
        return idx * 3 * inc

    return idx * 4 * inc


def intervals_len(intervals):
    sum = 0
    for s, e in intervals:
        sum += e - s + 1

    return sum


def isPrime(x2):
    x = BV2Int(x2, False)
    y, z = Ints("y z")
    return And(x > 1, Not(Exists([y, z], And(y < x, z < x, y > 1, z > 1, x == y * z))))
    # x2 in primes????

def solve_char(arg):
    i, needed_idx = arg
    # print(f"Analyzing {i} - needed {needed_idx} {chr(needed_idx)}")

    from_min, from_max, from_sort, exp = BitVecs('from_min from_max from_sort exp', 64)
    s = Solver()
    s.add(func(from_min, from_max, from_sort, exp, i) == needed_idx)
    s.add(exp > 1000, exp < PRIMES_UPPER_BOUND, isPrime(exp))
    s.add(from_min < 300_000, from_min > 10_000)
    s.add(from_max > 700_000, from_max < MAX_NUM)
    s.add(from_sort > 200_000, from_sort < 800_000)

    while s.check() == sat:
        m = s.model()
        fmin = m[from_min].as_long()
        fmax = m[from_max].as_long()
        fsort = m[from_sort].as_long()
        e = m[exp].as_long()
        s.add(Or(from_min != fmin, from_max != fmax, from_sort != fsort, exp != e))

        # print(fmin, fmax, fsort, e)
        if func(fmin, fmax, fsort, e, i) != needed_idx: continue

        fmin_intervals = MinCollector(ramper(300, 1500, i), fmin, i).get_shuffled()
        fmax_intervals = MaxCollector(ramper(200, 1200, i), fmax, i).get_shuffled()
        fsort_intervals = SortCollector(ramper(80, 400, i), fsort, i).get_shuffled()
        d_intervals = XorCollector2(ramper(100, 400, i), e, i).get_shuffled()

        # fmin_intervals = MinCollector(ramper(20, 0, i), fmin, i).get_shuffled()
        # fmax_intervals = MaxCollector(ramper(20, 0, i), fmax, i).get_shuffled()
        # fsort_intervals = SortCollector(ramper(20, 0, i), fsort, i).get_shuffled()
        # d_intervals = XorCollector2(ramper(20, 0, i), e, i).get_shuffled()

        if any(x is None for x in [fmin_intervals, fmax_intervals, fsort_intervals, d_intervals]):
            print(f"{i} looking for different solution")
            continue

        intervals = [fmin_intervals, fmax_intervals, fsort_intervals, d_intervals]
        picked_numbers = [fmin, fmax, fsort, e]
        break
    else:
        return None, None

    return intervals, picked_numbers


def get_lengths(*intervals):
    l = []
    for i in intervals:
        l.append(intervals_len(i))

    return ' '.join(map(str, l))


if __name__ == '__main__':
    flag = "justCTF{1_4m_5l0w_4nd_7h3_fl4g_15_l0ng_bu7_1_h0p3_y0u_0b53rv3d_m3_c4r3fu11y}"
    print(f'flag: {flag} {len(flag)} chars')
    needed_indices = list(map(ord, flag))

    challenge_data = []
    picked_numbers = []
    with Pool(6) as pool:
        for i, (intervals, selected_numbers) in enumerate(pool.imap(solve_char, enumerate(needed_indices))):
            if intervals is None or selected_numbers is None:
                raise SystemExit(f"No solution for {i}")

            print(f'{i}. {get_lengths(*intervals)}')
            challenge_data.append(intervals)
            picked_numbers.append(selected_numbers)

    with open("src/chall_data.hpp", "wt") as f:
        f.write(Template(Path("chall_data.jinja2").read_text()).render(
            challenge_data=challenge_data
        ))

    with open("src/verify_data.hpp", "wt") as f:
        f.write(Template(Path("chall_verify.jinja2").read_text()).render(
            picked_numbers=picked_numbers
        ))
