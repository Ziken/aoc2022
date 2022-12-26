import math
import re
from enum import Enum


class Material(int, Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4


class BackpackDifference(dict):
    def difference(self, backpack1, backpack2):
        for material in Material:
            self[material] = backpack1[material] - backpack2[material]


def go_to_next_minute(
    time_limit,
    backpack: dict,
    robots: dict,
    blueprint: dict,
    limits: dict,
    current_minute,
):
    if current_minute == time_limit:
        return backpack.copy()
    if current_minute > time_limit or any([robots[m] > l for m, l in limits.items()]):
        return {
            Material.ORE: 0,
            Material.CLAY: 0,
            Material.OBSIDIAN: 0,
            Material.GEODE: 0,
        }

    best_backpack = backpack
    for robot_type, cost in blueprint.items():
        needed_minutes = 1
        new_backpack = backpack.copy()
        can_build = True
        for material, amount in cost.items():
            if robots[material] == 0:
                can_build = False
                break

            needed_minutes = max(
                needed_minutes,
                math.ceil((amount - backpack[material]) / robots[material]) + 1,
            )
            new_backpack[material] -= amount
        if not can_build:
            continue

        for robot, production in robots.items():
            new_backpack[int(robot)] += needed_minutes * robots[robot]
        new_robots = robots.copy()
        new_robots[robot_type] += 1
        returned_backpack = go_to_next_minute(
            time_limit,
            new_backpack,
            new_robots,
            blueprint,
            limits,
            current_minute + needed_minutes,
        )
        if returned_backpack[Material.GEODE] > best_backpack[Material.GEODE]:
            best_backpack = returned_backpack

    b = backpack.copy()
    for robot, production in robots.items():
        b[int(robot)] += production * (time_limit - current_minute)

    if b[Material.GEODE] > best_backpack[Material.GEODE]:
        best_backpack = b

    return best_backpack


def get_limits(blueprint):
    limits = {
        Material.ORE: 0,
        Material.CLAY: 0,
        Material.OBSIDIAN: 0,
    }
    for r, cost in blueprint.items():
        for material, amount in cost.items():
            limits[material] = max(limits[material], amount)

    return limits


def part_1(blueprints):
    result = 0
    for i, blueprint in enumerate(blueprints):
        limits = get_limits(blueprint)

        best_backpack = go_to_next_minute(
            24,
            {
                Material.ORE: 0,
                Material.CLAY: 0,
                Material.OBSIDIAN: 0,
                Material.GEODE: 0,
            },
            {
                Material.ORE: 1,
                Material.CLAY: 0,
                Material.OBSIDIAN: 0,
                Material.GEODE: 0,
            },
            blueprint,
            limits,
            0,
        )
        result += best_backpack[Material.GEODE] * (i + 1)

    return result


def part_2(blueprints):
    result = 1
    for blueprint in blueprints[:3]:
        print("blueprint")
        limits = get_limits(blueprint)

        best_backpack = go_to_next_minute(
            32,
            {
                Material.ORE: 0,
                Material.CLAY: 0,
                Material.OBSIDIAN: 0,
                Material.GEODE: 0,
            },
            {
                Material.ORE: 1,
                Material.CLAY: 0,
                Material.OBSIDIAN: 0,
                Material.GEODE: 0,
            },
            blueprint,
            limits,
            0,
        )
        result *= best_backpack[Material.GEODE]

    return result


with open("19_input.txt") as f:
    raw_input = f.read().strip().splitlines()

blueprints = []
for line in raw_input:
    prices = re.findall(r"(\d+)", line)
    blueprint = {
        Material.ORE: {
            Material.ORE: int(prices[1]),
        },
        Material.CLAY: {
            Material.ORE: int(prices[2]),
        },
        Material.OBSIDIAN: {
            Material.ORE: int(prices[3]),
            Material.CLAY: int(prices[4]),
        },
        Material.GEODE: {
            Material.ORE: int(prices[5]),
            Material.OBSIDIAN: int(prices[6]),
        },
    }
    blueprints.append(blueprint)

print("Part 1", part_1(blueprints))
print("Part 2", part_2(blueprints))
