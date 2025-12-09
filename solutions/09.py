from dataclasses import dataclass
from itertools import combinations

with open("input/09.txt", encoding="utf8") as f:
    lines = f.read().splitlines()
    red_tiles = [(int(x), int(y)) for line in lines for x, y in [line.split(",")]]
    number_of_red_tiles = len(red_tiles)


def calculate_area(x1: int, y1: int, x2: int, y2: int):
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def get_vertical_edges() -> list[tuple[int, int, int]]:
    vertical_edges = []

    for i in range(number_of_red_tiles):
        (x1, y1) = red_tiles[i]
        (x2, y2) = red_tiles[(i + 1) % number_of_red_tiles]

        if x1 == x2:
            y_low, y_high = sorted((y1, y2))
            vertical_edges.append((x1, y_low, y_high))

    return vertical_edges


@dataclass
class Band:
    y_from: int
    y_to: int
    intervals: list[tuple[int, int]]


def get_bands() -> list[Band]:
    yx_bands = []

    vertical_edges = get_vertical_edges()
    ys = sorted({y for _, y, _ in vertical_edges})

    for y_from, y_next in zip(ys, ys[1:]):
        y_to = y_next - 1
        if y_from > y_to:
            continue

        y_mid = y_from

        xs = sorted(x for x, y_low, y_high in vertical_edges if y_low <= y_mid < y_high)

        intervals = [(a, b - 1) for a, b in zip(xs[0::2], xs[1::2])]

        yx_bands.append(Band(y_from, y_to, intervals))

    return yx_bands


def interval_is_covered(
    intervals: list[tuple[int, int]], x_low: int, x_high: int
) -> bool:
    needed = x_low

    for start, end in intervals:
        if end < needed:
            continue

        if start > needed:
            return False

        needed = end + 1
        if needed > x_high:
            return True

    return needed > x_high


def is_rectangle_inside(x1: int, y1: int, x2: int, y2: int, bands: list[Band]) -> bool:
    x_low, x_high = sorted((x1, x2))
    y_low, y_high = sorted((y1, y2))

    for band in bands:
        if band.y_to <= y_low or band.y_from >= y_high:
            continue
        if not interval_is_covered(band.intervals, x_low, x_high):
            return False
    return True


def part1():
    return max(
        calculate_area(x1, y1, x2, y2)
        for i, (x1, y1) in enumerate(red_tiles)
        for (x2, y2) in red_tiles[i + 1 :]
    )


def part2():
    bands = get_bands()

    return max(
        calculate_area(x1, y1, x2, y2)
        for (x1, y1), (x2, y2) in combinations(red_tiles, 2)
        if all({x1 != x2, y1 != y2, is_rectangle_inside(x1, y1, x2, y2, bands)})
    )


print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
