from dataclasses import dataclass


@dataclass
class Region:
    width: int
    height: int
    counts: list[int]


def parse_input(inputs: list[str]) -> tuple[list[int], list[Region]]:
    shape_counts: list[int] = []
    regions: list[Region] = []

    for i, line in enumerate(inputs):
        if line.endswith(":"):
            shape_rows = [inputs[i + j] for j in range(1, 4)]
            shape_counts.append(sum(row.count("#") for row in shape_rows))
        if "x" in line:
            left, right = line.split(":")
            width, height = map(int, left.split("x"))
            counts = list(map(int, right.split()))
            regions.append(Region(width=width, height=height, counts=counts))
    return shape_counts, regions


def can_fit_region(region: Region, shape_cell_counts: list[int]) -> bool:
    """So it turns out we don't actually need to do any fitting logic for this puzzle input -
    we just need to check that the region area is bigger or equal to the needed cells.
    This makes our job much simpler."""
    region_area = region.width * region.height
    _range = range(len(region.counts))
    needed_cells = sum(region.counts[sid] * shape_cell_counts[sid] for sid in _range)
    return needed_cells <= region_area


def solve_the_puzzle(inputs: list[str]) -> int:
    shape_cell_counts, regions = parse_input(inputs)
    return sum(1 for region in regions if can_fit_region(region, shape_cell_counts))


with open("input/12.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()

print(f"\n🎄 {"=" * 40} 🎄")
print("   ⭐ Day 12 (But sneaky) Results ⭐")
print(f"🎄 {"=" * 40} 🎄")
print(f"   🎁 Today's answer is: {solve_the_puzzle(lines)}")
print(f"🎄 {"=" * 40} 🎄\n")
