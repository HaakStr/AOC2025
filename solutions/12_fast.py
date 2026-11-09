import sys
from dataclasses import dataclass

Cells = frozenset[tuple[int, int]]


@dataclass
class Region:
    width: int
    height: int
    counts: list[int]


def parse_input(inputs: list[str]) -> tuple[list[Cells], list[Region]]:
    shapes: list[Cells] = []
    regions: list[Region] = []
    i = 0
    while i < len(inputs):
        line = inputs[i].strip()
        if line.endswith(":") and line[:-1].isdigit():
            rows = inputs[i + 1 : i + 4]
            shapes.append(
                frozenset(
                    (x, y)
                    for y, row in enumerate(rows)
                    for x, ch in enumerate(row)
                    if ch == "#"
                )
            )
            i += 4
        elif "x" in line and ":" in line:
            left, right = line.split(":", 1)
            w, h = map(int, left.split("x"))
            regions.append(Region(w, h, list(map(int, right.split()))))
            i += 1
        else:
            i += 1
    return shapes, regions


def normalize(cells: Cells) -> Cells:
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return frozenset((x - min_x, y - min_y) for x, y in cells)


def unique_orientations(cells: Cells) -> list[Cells]:
    out: set[Cells] = set()
    for base in (cells, frozenset((-x, y) for x, y in cells)):
        c = normalize(base)
        for _ in range(4):
            out.add(c)
            c = normalize(frozenset((y, -x) for x, y in c))
    return list(out)


def placements(width: int, height: int, orientations: list[Cells]) -> list[int]:
    masks: set[int] = set()
    for cells in orientations:
        max_x = max(x for x, _ in cells) + 1
        max_y = max(y for _, y in cells) + 1
        for oy in range(height - max_y + 1):
            for ox in range(width - max_x + 1):
                masks.add(sum(1 << ((oy + y) * width + ox + x) for x, y in cells))
    return list(masks)


def search(region: Region, orients: list[list[Cells]], cell_counts: list[int]) -> bool:
    n = len(region.counts)
    area = region.width * region.height
    all_placements = [
        placements(region.width, region.height, orients[s]) for s in range(n)
    ]

    def dfs(occ: int, remaining: tuple[int, ...], avail: list[list[int]]) -> bool:
        if not any(remaining):
            return True
        if (
            sum(r * c for r, c in zip(remaining, cell_counts, strict=False))
            > area - occ.bit_count()
        ):
            return False

        # Filter once per node and hand the shrunken lists to the children
        avail = [
            [m for m in avail[s] if not m & occ] if remaining[s] else []
            for s in range(n)
        ]
        best = -1
        for s in range(n):
            if remaining[s]:
                if not avail[s]:
                    return False
                if best < 0 or len(avail[s]) < len(avail[best]):
                    best = s

        next_remaining = (
            remaining[:best] + (remaining[best] - 1,) + remaining[best + 1 :]
        )
        return any(dfs(occ | m, next_remaining, avail) for m in avail[best])

    return dfs(0, tuple(region.counts), all_placements)


def can_fit_region(
    region: Region, orients: list[list[Cells]], cell_counts: list[int]
) -> bool:
    area = region.width * region.height
    needed = sum(c * n for c, n in zip(region.counts, cell_counts, strict=False))
    if needed > area:
        return False

    # Every shape fits in a 3x3 box, so if there is a free box per piece, it always works
    if sum(region.counts) <= (region.width // 3) * (region.height // 3):
        return True

    return search(region, orients, cell_counts)


def solve_the_puzzle(inputs: list[str]) -> int:
    shapes, regions = parse_input(inputs)
    orients = [unique_orientations(s) for s in shapes]
    cell_counts = [len(s) for s in shapes]
    return sum(can_fit_region(r, orients, cell_counts) for r in regions)


sys.setrecursionlimit(10_000)

with open("input/12.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()

print(f"\n🎄 {'=' * 40} 🎄")
print("   ⭐ Day 12 (Fast) Results ⭐")
print(f"🎄 {'=' * 40} 🎄")
print(f"   🎁 Today's answer is: {solve_the_puzzle(lines)}")
print(f"🎄 {'=' * 40} 🎄\n")
