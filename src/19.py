import argparse
import re
from typing import Dict, List, Tuple, cast

from tqdm import tqdm

from utils import get_input

BLUEPRINT_ID = r"Blueprint (\d+)"
ORE_ROBOT_COST = r"Each ore robot costs (\d+) ore."
CLAY_ROBOT_COST = r" Each clay robot costs (\d+) ore."
OBSIDIAN_ROBOT_COST = r"Each obsidian robot costs (\d+) ore and (\d+) clay."
GEODE_ROBOT_COST = r"Each geode robot costs (\d+) ore and (\d+) obsidian."

Blueprint = Tuple[int, int, Tuple[int, int], Tuple[int, int]]

State = Tuple[int, int, int, int, int, int, int, int, int]

memo: Dict[State, int] = {}


def parse_input(input: List[str]) -> List[Blueprint]:
    blueprints: List[Blueprint] = []
    for line in input:
        ore_robot_cost = re.search(ORE_ROBOT_COST, line).group(1)  # type: ignore
        clay_robot_cost = re.search(CLAY_ROBOT_COST, line).group(1)  # type: ignore
        obsidian_robot_cost = re.search(
            OBSIDIAN_ROBOT_COST, line
        ).groups()  # type: ignore
        geode_robot_cost = re.search(GEODE_ROBOT_COST, line).groups()  # type: ignore
        blueprints.append(
            (
                int(ore_robot_cost),
                int(clay_robot_cost),
                cast(Tuple[int, int], tuple(int(a) for a in obsidian_robot_cost)),
                cast(Tuple[int, int], tuple(int(a) for a in geode_robot_cost)),
            )
        )
    return blueprints


def iterate(
    state: State,
    blueprint: Blueprint,
) -> int:
    if state in memo:
        return memo[state]
    (
        minute,
        ore,
        ore_robots,
        clay,
        clay_robots,
        obsidian,
        obsidian_robots,
        geode,
        geode_robots,
    ) = state
    if minute <= 0:
        memo[state] = geode
        return geode
    (
        ore_robot_cost,
        clay_robot_cost,
        (obsidian_robot_cost_ore, obsidian_robot_cost_clay),
        (geode_robot_cost_ore, geode_robot_cost_obsidian),
    ) = blueprint

    possible_states: List[int] = []
    # If we can make any robot
    if ore >= geode_robot_cost_ore and obsidian >= geode_robot_cost_obsidian:
        # Create a geode robot
        possible_states.append(
            iterate(
                (
                    minute - 1,
                    ore - geode_robot_cost_ore + ore_robots,
                    ore_robots,
                    clay + clay_robots,
                    clay_robots,
                    obsidian - geode_robot_cost_obsidian + obsidian_robots,
                    obsidian_robots,
                    geode + geode_robots,
                    geode_robots + 1,
                ),
                blueprint,
            )
        )
    else:
        if ore >= obsidian_robot_cost_ore and clay >= obsidian_robot_cost_clay:
            # Create a obsidian robot
            possible_states.append(
                iterate(
                    (
                        minute - 1,
                        ore - obsidian_robot_cost_ore + ore_robots,
                        ore_robots,
                        clay - obsidian_robot_cost_clay + clay_robots,
                        clay_robots,
                        obsidian + obsidian_robots,
                        obsidian_robots + 1,
                        geode + geode_robots,
                        geode_robots,
                    ),
                    blueprint,
                )
            )
        else:
            possible_states.append(
                iterate(
                    (
                        minute - 1,
                        ore + ore_robots,
                        ore_robots,
                        clay + clay_robots,
                        clay_robots,
                        obsidian + obsidian_robots,
                        obsidian_robots,
                        geode + geode_robots,
                        geode_robots,
                    ),
                    blueprint,
                )
            )
            if ore >= clay_robot_cost:
                # Create a clay robot
                possible_states.append(
                    iterate(
                        (
                            minute - 1,
                            ore - clay_robot_cost + ore_robots,
                            ore_robots,
                            clay + clay_robots,
                            clay_robots + 1,
                            obsidian + obsidian_robots,
                            obsidian_robots,
                            geode + geode_robots,
                            geode_robots,
                        ),
                        blueprint,
                    )
                )
            if ore >= ore_robot_cost:
                # Create an ore robot
                possible_states.append(
                    iterate(
                        (
                            minute - 1,
                            ore - ore_robot_cost + ore_robots,
                            ore_robots + 1,
                            clay + clay_robots,
                            clay_robots,
                            obsidian + obsidian_robots,
                            obsidian_robots,
                            geode + geode_robots,
                            geode_robots,
                        ),
                        blueprint,
                    )
                )
    # Return the state that gives most geode
    maximum = max(possible_states)
    memo[state] = maximum
    return maximum


if __name__ == "__main__":
    blueprints = parse_input(get_input(19, False, strip=True))
    result: int = 0
    parser = argparse.ArgumentParser(prog="AOC day 19")
    parser.add_argument("part", type=int, default=1)
    args = parser.parse_args()
    if args.part == 1:
        progress = tqdm(total=len(blueprints))
        for i, blueprint in enumerate(blueprints):
            memo = {}
            best_state = iterate((24, 0, 1, 0, 0, 0, 0, 0, 0), blueprint)
            result += (i + 1) * best_state
            progress.update(1)
        print(f"Part 1: {result}")
    elif args.part == 2:
        result = 1
        progress = tqdm(total=3)
        for i, blueprint in enumerate(blueprints[:3]):
            memo = {}
            best_state = iterate((32, 0, 1, 0, 0, 0, 0, 0, 0), blueprint)
            print(best_state)
            result *= best_state
            progress.update(1)
        print(f"Part 2: {result}")
