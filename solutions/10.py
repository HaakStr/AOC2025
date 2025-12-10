from collections import deque
from dataclasses import dataclass
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np


@dataclass
class Machine:
    indicators: list[str]
    buttons: list[tuple[int, ...]]
    joltage: list[int]


def create_machine(line: str) -> Machine:
    indicator_parts = []
    buttons: list[tuple[int, ...]] = []
    joltage = []

    for part in line.split():
        match part[0]:
            case "[":
                indicator_parts = list(part.strip("]["))
            case "(":
                buttons.append(tuple(map(int, part.strip(")(").split(","))))
            case "{":
                joltage = list(map(int, part.strip("}{").split(",")))
            case _:
                raise ValueError(f"Unknown part format: {part}")

    return Machine(indicator_parts, buttons, joltage)


with open("input/10.txt", encoding="utf-8") as file:
    machines: list[Machine] = [
        create_machine(line.strip()) for line in file if line.strip()
    ]


def fewest_presses(machine: Machine) -> int:
    target = 0
    for i, ch in enumerate(machine.indicators):
        if ch == "#":
            target |= 1 << i

    button_masks: list[int] = []
    for btn in machine.buttons:
        mask = 0
        for idx in btn:
            # Slide them bits
            mask |= 1 << idx
        button_masks.append(mask)

    dist = [0] + [-1] * ((1 << len(machine.indicators)) - 1)
    queue = deque({0})

    while queue:
        state = queue.popleft()

        for bmask in button_masks:
            # Toggle them bits
            new_state = state ^ bmask
            if dist[new_state] == -1:
                dist[new_state] = dist[state] + 1
                if new_state == target:
                    return dist[new_state]
                queue.append(new_state)

    # Not technically necessary. Just need the type checker to be happy.
    raise ValueError("No solution found")


def reduce_machine_for_joltage(
    machine: Machine,
) -> tuple[list[tuple[int, ...]], list[int]]:
    target = machine.joltage[:]
    important_indices = [i for i, t in enumerate(target) if t > 0]
    old_to_new = {old: new for new, old in enumerate(important_indices)}

    new_buttons = [
        tuple(sorted(set(old_to_new[i] for i in btn if i in old_to_new)))
        for btn in [tuple(btn) for btn in machine.buttons]
        if any(i in old_to_new for i in btn)
    ]

    return new_buttons, [target[old] for old in important_indices]


def solve_joltage_milp(buttons: list[tuple[int, ...]], target: list[int]):
    n_buttons = len(buttons)

    array = np.zeros((len(target), n_buttons))
    for btn_idx, btn in enumerate(buttons):
        for counter_idx in btn:
            array[counter_idx, btn_idx] = 1

    ones = np.ones(n_buttons)

    result = milp(
        ones,
        bounds=Bounds(lb=0, ub=max(target) * 2),
        constraints=LinearConstraint(array, lb=target, ub=target),  # type: ignore
        integrality=ones,
    )
    if result.success:
        return int(result.fun)

    raise ValueError("MILP solver failed")


def fewest_presses_with_joltage(machine: Machine) -> int:
    """It's MILP'in time."""
    buttons, target = reduce_machine_for_joltage(machine)

    return solve_joltage_milp(buttons, target)


def part1():
    return sum(fewest_presses(machine) for machine in machines)


def part2():
    return sum(fewest_presses_with_joltage(machine) for machine in machines)


print(f"\n🎄 {"="*40} 🎄")
print(
    f"   ⭐ Day {int(__file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]):02d} Results ⭐"
)
print(f"🎄 {"="*40} 🎄")
print(f"   🎁 Part 1: {part1()}")
print(f"   🎁 Part 2: {part2()}")
print(f"🎄 {"="*40} 🎄\n")
