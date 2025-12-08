with open("input/02.txt", encoding="utf-8") as f:
    lines = f.read().strip().split(",")
    ranges = [(int(x[0]), int(x[1])) for x in (line.split("-") for line in lines)]


def is_a_number_repeated_twice(s: str) -> bool:
    length = len(s)
    mid = length // 2

    return length % 2 == 0 and s[:mid] == s[mid:]


def is_a_number_repeated_atleast_twice(s: str) -> bool:
    length = len(s)

    return any(
        s[:seq_length] * (length // seq_length) == s
        for seq_length in range(1, length // 2 + 1)
        if length % seq_length == 0
    )


invalid_number_sum = 0
invalid_number_sum_2 = 0

for start, end in ranges:
    for n in range(start, end + 1):
        number_string = str(n)
        if is_a_number_repeated_twice(number_string):
            invalid_number_sum += n
        if is_a_number_repeated_atleast_twice(number_string):
            invalid_number_sum_2 += n

print("\n🎄 ======================================= 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print("🎄 ======================================= 🎄")
print(f"   🎁 Part 1: {invalid_number_sum}")
print(f"   🎁 Part 2: {invalid_number_sum_2}")
print("🎄 ======================================= 🎄\n")
