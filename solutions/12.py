from dataclasses import dataclass


@dataclass
class Region:
    width: int
    height: int
    counts: list[int]


class RegionProgress:
    def __init__(self, desc: str):
        self.desc = desc
        self.count = 0
        self._found_printed = False

    def tick(self):
        self.count += 1
        print(f"{self.desc} - Checking #{self.count}", end="\r")

    def found(self):
        if self._found_printed:
            return
        self._found_printed = True
        print(f"{self.desc} - ✅ Match found after {self.count} DFS iterations")

    def close(self):
        if not self._found_printed:
            print()


def parse_input(inputs: list[str]) -> tuple[list[dict], list[Region]]:
    shapes: list[dict] = []
    regions: list[Region] = []
    i = 0
    while i < len(inputs):
        line = inputs[i].strip()
        if line and ":" in line and line[:-1].isdigit():
            sid = int(line[:-1])
            pattern = [inputs[i + j].rstrip("\n") for j in range(1, 4)]
            shapes.append({"id": sid, "pattern": pattern})
            i += 4
            continue
        if line and "x" in line and ":" in line:
            left, right = line.split(":", 1)
            w_str, h_str = left.strip().split("x")
            w, h = int(w_str), int(h_str)
            counts = list(map(int, right.strip().split()))
            regions.append(Region(width=w, height=h, counts=counts))
            i += 1
            continue
        i += 1
    return shapes, regions


def shape_cells_from_pattern(pattern: list[str]) -> frozenset[tuple[int, int]]:

    return frozenset(
        (x, y)
        for y, row in enumerate(pattern)
        for x, ch in enumerate(row.strip())
        if ch == "#"
    )


def normalize(cells: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    return frozenset(
        (x - min(x for x, _ in cells), y - min(y for _, y in cells)) for x, y in cells
    )


def rot90(cells: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    return normalize(frozenset((y, -x) for x, y in cells))


def flip_x(cells: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    return normalize(frozenset((-x, y) for x, y in cells))


def unique_orientations(
    cells: frozenset[tuple[int, int]],
) -> list[frozenset[tuple[int, int]]]:
    out = set()
    c = normalize(cells)
    for _ in range(4):
        out.add(c)
        c = rot90(c)
    c = flip_x(normalize(cells))
    for _ in range(4):
        out.add(c)
        c = rot90(c)
    return list(out)


def placements_bitmasks(
    W: int,
    H: int,
    oriented_cells: frozenset[tuple[int, int]],
) -> tuple[int, ...]:
    maxx = max(x for x, _ in oriented_cells) + 1
    maxy = max(y for _, y in oriented_cells) + 1

    masks = []
    for oy in range(H - maxy + 1):
        for ox in range(W - maxx + 1):
            m = 0
            for x, y in oriented_cells:
                idx = (oy + y) * W + (ox + x)
                m |= 1 << idx
            masks.append(m)
    return tuple(masks)


def can_fit_region(
    region: Region,
    shape_orients: list[list[frozenset[tuple[int, int]]]],
    shape_cell_counts: list[int],
    region_idx: int,
) -> bool:
    n_shapes = len(region.counts)
    area_total = region.width * region.height
    need_cells = sum(
        region.counts[sid] * shape_cell_counts[sid] for sid in range(n_shapes)
    )
    if need_cells > area_total:
        print(
            f"Region {region_idx}: {region.width}x{region.height} -"
            f" ⏭️ Skipped (needs {need_cells} cells; has {area_total})"
        )
        return False

    placements: list[list[int]] = [[] for _ in range(n_shapes)]
    for sid in range(n_shapes):
        seen = set()
        for oc in shape_orients[sid]:
            for m in placements_bitmasks(region.width, region.height, oc):
                if m not in seen:
                    seen.add(m)
                    placements[sid].append(m)

    progress = RegionProgress(f"Region {region_idx}: {region.width}x{region.height}")

    def dfs(occ: int, remaining: tuple[int, ...]) -> bool:
        if sum(remaining) == 0:
            return True

        free = area_total - occ.bit_count()
        rem_cells = sum(
            remaining[sid] * shape_cell_counts[sid] for sid in range(n_shapes)
        )
        if rem_cells > free:
            return False

        best_sid = -1
        best_count = float("inf")

        for sid in range(n_shapes):
            if remaining[sid] == 0:
                continue

            count = sum(1 for m in placements[sid] if (m & occ) == 0)

            if count == 0:
                return False

            if count < best_count:
                best_count = count
                best_sid = sid
                if count == 1:
                    break

        valid_placements = [m for m in placements[best_sid] if (m & occ) == 0]

        new_remaining = list(remaining)
        new_remaining[best_sid] -= 1
        new_remaining = tuple(new_remaining)

        for m in valid_placements:
            progress.tick()
            if dfs(occ | m, new_remaining):
                progress.found()
                return True

        return False

    result = dfs(0, tuple(region.counts))
    progress.close()
    return result


def solve_the_puzzle(inputs: list[str]) -> int:
    shapes, regions = parse_input(inputs)
    sorted_shapes = sorted(shapes, key=lambda s: s["id"])
    shape_orients = [
        unique_orientations(shape_cells_from_pattern(s["pattern"]))
        for s in sorted_shapes
    ]
    shape_cell_counts = [
        len(shape_orients[sid][0]) for sid in range(len(shape_orients))
    ]

    return sum(
        1
        for i, r in enumerate(regions, 1)
        if can_fit_region(r, shape_orients, shape_cell_counts, i)
    )


with open("input/12.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()


puzzle_result = solve_the_puzzle(lines)
print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Today's answer is: {puzzle_result}")
print(f"🎄 {"="*40} 🎄\n")
