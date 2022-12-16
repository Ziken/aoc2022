import dataclasses
import re
from typing import List
from dataclasses import dataclass

line_regexp = re.compile(r"([A-Z]{2}|\d+)")

with open("16_input.txt") as f:
    raw_input = f.read().strip().splitlines()


@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: List[str] = dataclasses.field(default_factory=list)


valves = dict()
for line in raw_input:
    name, flow_rate, *tunnels = line_regexp.findall(line)
    valves[name] = Valve(name, int(flow_rate), tunnels)

full_valves = [v.name for v in valves.values() if v.flow_rate > 0]


def optimized_traverse_graph(
    current_valve: Valve, visited: List[str], current_pressure=0, minute=0
) -> int:
    cost_table = dict()
    calculate_costs(current_valve, cost_table)
    this_visited_valves = []
    max_pressure = current_pressure
    for nv in full_valves:
        if nv in visited:
            continue

        next_valve = valves[nv]

        this_visited_valves.append(next_valve.name)

        cost, _ = cost_table[next_valve.name]
        if minute + cost > 30:
            return max_pressure

        new_pressure = current_pressure + (30 - cost - minute) * next_valve.flow_rate
        calculated_pressure = optimized_traverse_graph(
            next_valve, visited + [next_valve.name], new_pressure, minute + cost
        )
        if calculated_pressure > max_pressure:
            # print(calculated_pressure)
            max_pressure = calculated_pressure

    return max_pressure


CACHED = dict()


def optimized_traverse_graph_with_two(
    current_valve_1: Valve,
    current_valve_2: Valve,
    visited: List[str],
    current_pressure=0,
    minute_1=0,
    minute_2=0,
) -> int:
    cost_table_1 = dict()
    calculate_costs(current_valve_1, cost_table_1)
    # by_cost_1 = sorted(cost_table_1, key=lambda x: cost_table_1[x][1], reverse=True)
    #
    cost_table_2 = dict()
    calculate_costs(current_valve_2, cost_table_2)
    # by_cost_2 = sorted(cost_table_2, key=lambda x: cost_table_2[x][1], reverse=True)
    #
    # this_visited_valves_1 = []
    # this_visited_valves_2 = []

    max_pressure = current_pressure
    for v1 in full_valves:
        if v1 in visited:
            continue
        for v2 in full_valves:
            if v2 in visited or v2 == v1:
                continue

            next_valve_1 = valves[v1]
            next_valve_2 = valves[v2]

            vvv = []
            cost_1, _ = cost_table_1[next_valve_1.name]
            if minute_1 + cost_1 > 26:
                new_pressure_1 = 0
                m1 = minute_1
                next_valve_1 = current_valve_1
            else:
                vvv.append(next_valve_1.name)
                new_pressure_1 = (26 - cost_1 - minute_1) * next_valve_1.flow_rate
                m1 = minute_1 + cost_1

            cost_2, _ = cost_table_2[next_valve_2.name]
            if minute_2 + cost_2 > 26:
                new_pressure_2 = 0
                m2 = minute_2
                next_valve_2 = current_valve_2
            else:
                vvv.append(next_valve_2.name)
                new_pressure_2 = (26 - cost_2 - minute_2) * next_valve_2.flow_rate
                m2 = minute_2 + cost_2


            if (minute_1 + cost_1 > 26) and (minute_2 + cost_2 > 26):
                return max_pressure

            if (
                next_valve_1.name,
                next_valve_2.name,
                tuple(visited + vvv),
                m1,
                m2,
            ) in CACHED:
                calculated_pressure = CACHED[
                    (next_valve_1.name, next_valve_2.name, tuple(visited + vvv), m1, m2)
                ]
            else:
                calculated_pressure = optimized_traverse_graph_with_two(
                    next_valve_1,
                    next_valve_2,
                    visited + vvv,
                    current_pressure + new_pressure_1 + new_pressure_2,
                    m1,
                    m2,
                )
                CACHED[
                    (next_valve_1.name, next_valve_2.name, tuple(visited + vvv), m1, m2)
                ] = calculated_pressure

            if calculated_pressure > max_pressure:
                max_pressure = calculated_pressure

    return max_pressure


def calculate_costs(valve: Valve, cost_table, current_cost=1):
    visited = {valve.name}
    to_visit = valve.tunnels
    if valve.flow_rate != 0:
        cost_table[valve.name] = (current_cost, valve.flow_rate / current_cost)

    while to_visit:
        current_cost += 1
        new_visit = []
        for tunnel in to_visit:
            if tunnel not in visited:
                new_visit.extend(valves[tunnel].tunnels)
            visited.add(tunnel)
            if valves[tunnel].flow_rate == 0:
                continue

            present_cost = cost_table.get(tunnel, (current_cost, 0))[0]
            if present_cost >= current_cost:
                cost_table[tunnel] = (
                    current_cost,
                    valves[tunnel].flow_rate / current_cost,
                )

        to_visit = new_visit


def part_1():
    return optimized_traverse_graph(valves["AA"], [])


def part_2():
    return optimized_traverse_graph_with_two(valves["AA"], valves["AA"], [], 0, 0, 0)


print("Part 1:", part_1())
print("Part 2:", part_2())


# 2924 -- too high
# 2848 -- too high
