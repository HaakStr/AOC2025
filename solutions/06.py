from math import prod

with open("input/06.txt", encoding="utf-8") as f:
    data = f.readlines()


def is_empty_column(rows: list[str], col: int):
    return all(rows[r][col] == " " for r in range(len(rows)))


def find_group_boundaries(rows: list[str], start_col: int):
    left = start_col
    while left >= 0 and not is_empty_column(rows, left):
        left -= 1
    return left + 1, start_col


def get_operation(rows: list[str], left: int, right: int):
    return (
        "*"
        if any(
            rows[r][c] == "*" for r in range(len(rows)) for c in range(left, right + 1)
        )
        else "+"
    )


def extract_numbers(rows: list[str], left: int, right: int):
    return [
        int("".join(rows[r][c] for r in range(len(rows) - 1) if rows[r][c].isdigit()))
        for c in range(left, right + 1)
    ]


def part1():

    rows = [line.split() for line in data]
    amount_of_rows = len(rows) - 1

    return sum(
        (
            prod(int(rows[row][i]) for row in range(amount_of_rows))
            if rows[-1][i] == "*"
            else sum(int(rows[row][i]) for row in range(amount_of_rows))
        )
        for i in range(len(rows[0]))
    )


def part2():
    rows = [line.rstrip("\n") for line in data]
    col = len(rows[0]) - 1

    total = 0

    while col >= 0:
        if is_empty_column(rows, col):
            col -= 1
            continue

        left, right = find_group_boundaries(rows, col)
        operation = get_operation(rows, left, right)
        numbers = extract_numbers(rows, left, right)

        total += prod(numbers) if operation == "*" else sum(numbers)
        col = left - 1

    return total


print(f"\n🎄 {"="*40} 🎄")
print(f"   ⭐ Day {2:02d} Results ⭐")
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
