with open("input/07.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()
    height = len(lines)
    width = len(lines[0])


def part1():
    grid = [list(line) for line in lines]
    activated_splitters: list[tuple[int, int]] = []

    for x, line in enumerate(grid):
        for y, char in enumerate(line):

            if char == "S":
                grid[x][y] = "|"

            if char == "^":
                if y > 0:
                    grid[x][y - 1] = "|"
                if y < width - 1:
                    grid[x][y + 1] = "|"

                if grid[x - 1][y] == "|":
                    activated_splitters.append((x, y))

            if char == "." and grid[x - 1][y] == "|":
                grid[x][y] = "|"

    return len(activated_splitters)


def part2():
    dyn_prog: list[list[int]] = [[0] * width for _ in range(height)]

    s_row, s_col = 0, lines[0].index("S")
    dyn_prog[s_row][s_col] = 1

    for row in range(height - 1):
        for col in range(width):
            paths = dyn_prog[row][col]
            if paths == 0:
                continue

            if lines[row + 1][col] == "^":
                if col > 0:
                    dyn_prog[row + 1][col - 1] += paths
                if col < width - 1:
                    dyn_prog[row + 1][col + 1] += paths
            else:
                dyn_prog[row + 1][col] += paths
    return sum(dyn_prog[height - 1])


print(f"\n🎄 {"="*40} 🎄")
print(f"   ⭐ Day {2:02d} Results ⭐")
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
