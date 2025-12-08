with open("input/08.txt", encoding="utf-8") as f:
    lines = f.readlines()
    xyz_coords = [
        (int(coord[0]), int(coord[1]), int(coord[2]))
        for coord in (line.strip().split(",") for line in lines)
    ]

    number_of_coords = len(xyz_coords)


def get_edges():
    edges: list[tuple[int, int, int]] = []
    for i in range(number_of_coords):
        x1, y1, z1 = xyz_coords[i]
        for j in range(i + 1, number_of_coords):
            x2, y2, z2 = xyz_coords[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            d2 = dx * dx + dy * dy + dz * dz
            edges.append((d2, i, j))
    edges.sort(key=lambda e: e[0])

    return edges


def make_dsu():
    """As we'll be doing union-find, we make a DSU-ish (Disjoint Set Union) structure.
    This will help us keep track of connected components per union operation.
    The DSU is created per part to avoid mutation between parts."""

    parent = list(range(number_of_coords))
    size = [1] * number_of_coords

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    return find, union


def part1():
    find, union = make_dsu()
    edges = get_edges()
    for k in range(1000):
        _, i, j = edges[k]
        union(i, j)

    component_sizes: dict[int, int] = {}

    for i in range(number_of_coords):
        root = find(i)
        component_sizes[root] = component_sizes.get(root, 0) + 1

    sizes = sorted(component_sizes.values(), reverse=True)
    result = sizes[0] * sizes[1] * sizes[2]

    return result


def part2():
    _, union = make_dsu()
    edges = get_edges()
    components = number_of_coords
    last_edge = (0, 0)

    for _, i, j in edges:
        if union(i, j):
            components -= 1
            if components == 1:
                last_edge = (i, j)
                break
    i, j = last_edge

    return xyz_coords[i][0] * xyz_coords[j][0]


print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
