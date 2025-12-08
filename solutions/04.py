with open("input/04.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()
    grid = [list(line) for line in lines]
    grid_height = len(grid)
    grid_width = len(grid[0])


def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    """Returns valid neighboring coordinates for (x, y) in the grid.
    Respects grid boundaries."""
    neighbors: list[tuple[int, int]] = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                neighbors.append((nx, ny))
    return neighbors


def part1():
    result = 0

    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char != "@":
                continue

            neighbors = get_neighbors(j, i)
            counter = sum(1 for nx, ny in neighbors if grid[ny][nx] == "@")

            if counter < 4:
                result += 1

    return result


def part2():
    result = 0
    has_removed = True

    while has_removed:
        has_removed = False

        for i, line in enumerate(grid):
            for j, char in enumerate(line):
                if char != "@":
                    continue

                neighbors = get_neighbors(j, i)
                counter = sum(1 for nx, ny in neighbors if grid[ny][nx] == "@")

                if counter < 4:
                    grid[i][j] = "."
                    result += 1
                    has_removed = True
    return result


print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
