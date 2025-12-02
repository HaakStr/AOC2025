with open("input/01.txt", encoding="utf-8") as f:
    data = f.read().split("\n")
    instructions = [(x[0], int(x[1:])) for x in data]


def simulate_dial(dial_instructions: list[tuple[str, int]], step_by_step=False) -> int:

    current_dial = 50
    times_the_dial_is_zero = 0

    for direction, value in dial_instructions:
        if step_by_step:
            step = -1 if direction == "L" else 1
            for _ in range(value):
                current_dial = (current_dial + step) % 100
                if current_dial == 0:
                    times_the_dial_is_zero += 1
        else:
            delta = -value if direction == "L" else value
            current_dial = (current_dial + delta) % 100
            if current_dial == 0:
                times_the_dial_is_zero += 1
    if step_by_step:
        return current_dial
    return times_the_dial_is_zero


print("\n🎄 ======================================= 🎄")
print(f"   ⭐ Day {1:02d} Results ⭐")
print("🎄 ======================================= 🎄")
print(f"   🎁 Part 1: {simulate_dial(instructions, step_by_step=False)}")
print(f"   🎁 Part 2: {simulate_dial(instructions, step_by_step=True)}")
print("🎄 ======================================= 🎄\n")
