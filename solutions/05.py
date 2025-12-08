with open("input/05.txt", encoding="utf8") as f:
    lines = f.read().splitlines()


def merge_ranges(unmerged_ranges: list[list[int]]):
    sorted_ranges = sorted(unmerged_ranges, key=lambda r: r[0])
    merged: list[list[int]] = []

    for start, end in sorted_ranges:
        if not merged:
            merged.append([start, end])
            continue

        _, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged


def get_ranges_and_ids():

    ranges_done = False
    ranges: list[list[int]] = []
    ids: set[int] = set()

    for line in lines:
        if not line:
            ranges_done = True
            continue

        if not ranges_done:
            range_s, range_e = line.split("-")
            ranges.append([int(range_s), int(range_e)])
        else:
            ids.add(int(line))

    return merge_ranges(ranges), ids


ingredient_ranges, ingredient_ids = get_ranges_and_ids()


def part1():

    return len(
        {
            ingredient_id
            for ingredient_id in ingredient_ids
            for range_start, range_end in ingredient_ranges
            if range_start <= ingredient_id <= range_end
        }
    )


def part2():
    return sum(end - start + 1 for start, end in ingredient_ranges)


print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
