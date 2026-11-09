from collections import defaultdict

with open("input/11.txt", encoding="utf-8") as f:
    links = {
        (device, output)
        for line in f.read().splitlines()
        for device, outputs in [line.split(":")]
        for output in outputs.split()
    }


def count_paths(
    edges: set[tuple[str, str]], start: str, must_visit: set[str] | None = None
) -> int:
    if must_visit is None:
        must_visit = set()

    graph: defaultdict[str, list[str]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    memory: dict[tuple[str, frozenset[str]], int] = {}

    def dfs(node: str, visited_required: frozenset[str]) -> int:
        if node == "out":
            return int(visited_required == must_visit)

        state = (node, visited_required)
        if state in memory:
            return memory[state]

        new_visited = (
            visited_required if node not in must_visit else visited_required | {node}
        )

        total = sum(dfs(neighbor, new_visited) for neighbor in graph[node])

        memory[state] = total
        return total

    return dfs(start, frozenset())


def part1():
    return count_paths(links, start="you")


def part2():
    return count_paths(links, start="svr", must_visit={"dac", "fft"})


print(f"\n🎄 {'=' * 40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split('.')[0]):02d} Results ⭐"
)
print(f"🎄 {'=' * 40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {'=' * 40} 🎄\n")
