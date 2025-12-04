with open("input/03.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()


def get_biggest_two_digit_number_brute_force_edition(battery_bank: str) -> int:

    biggest_number = 0

    for i, char1 in enumerate(battery_bank):
        for j, char2 in enumerate(battery_bank):
            if i < j:
                biggest_number = max(biggest_number, int(char1 + char2))

    return biggest_number


def get_biggest_twelve_digit_number_crime_edition(battery_bank: str) -> int:
    biggest_number = 0

    for i, char1 in enumerate(battery_bank):
        for j, char2 in enumerate(battery_bank):
            for k, char3 in enumerate(battery_bank):
                for l, char4 in enumerate(battery_bank):
                    for m, char5 in enumerate(battery_bank):
                        for n, char6 in enumerate(battery_bank):
                            for o, char7 in enumerate(battery_bank):
                                for p, char8 in enumerate(battery_bank):
                                    for q, char9 in enumerate(battery_bank):
                                        for r, char10 in enumerate(battery_bank):
                                            for s, char11 in enumerate(battery_bank):
                                                for t, char12 in enumerate(
                                                    battery_bank
                                                ):
                                                    if all(
                                                        [
                                                            i < j,
                                                            j < k,
                                                            k < l,
                                                            l < m,
                                                            m < n,
                                                            n < o,
                                                            o < p,
                                                            p < q,
                                                            q < r,
                                                            r < s,
                                                            s < t,
                                                        ]
                                                    ):
                                                        biggest_number = max(
                                                            biggest_number,
                                                            int(
                                                                char1
                                                                + char2
                                                                + char3
                                                                + char4
                                                                + char5
                                                                + char6
                                                                + char7
                                                                + char8
                                                                + char9
                                                                + char10
                                                                + char11
                                                                + char12
                                                            ),
                                                        )

    return biggest_number


def get_biggest_k_digit_number(battery_bank: str, k: int) -> int:
    """Final result. Generalized function to get the biggest k digit number from the battery bank
    string. Uses a greedy algorithm to select the largest digit within the constraints.
    """
    result = []
    start = 0

    for remaining in range(k, 0, -1):
        end = len(battery_bank) - remaining + 1
        next_digit = max(battery_bank[start:end])
        result.append(next_digit)
        start = battery_bank.index(next_digit, start) + 1

    return int("".join(result))


two_digit_number_sum = 0
twelve_digit_number_sum = 0

for bank in lines:
    two_digit_number_sum += get_biggest_k_digit_number(bank, 2)
    twelve_digit_number_sum += get_biggest_k_digit_number(bank, 12)

print("\n🎄 ======================================= 🎄")
print(f"   ⭐ Day {2:02d} Results ⭐")
print("🎄 ======================================= 🎄")
print(f"   🎁 Part 1: {two_digit_number_sum}")
print(f"   🎁 Part 2: {twelve_digit_number_sum}")
print("🎄 ======================================= 🎄\n")
