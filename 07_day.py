import dataclasses
from typing import Optional


@dataclasses.dataclass
class File:
    is_dir: bool
    name: str
    size: Optional[int] = None
    parent: Optional["File"] = None
    files: list["File"] = dataclasses.field(default_factory=list)


def print_tree(file: File, indent=0):
    print("  " * indent, file.name, file.size)
    for sub_file in file.files:
        print_tree(sub_file, indent + 1)


def calc_dir_size(file: File):
    if file.is_dir:
        s = sum(calc_dir_size(sub_file) for sub_file in file.files)
        file.size = s
        return s
    else:
        return file.size


def part_1(file: File):
    s = 100000
    result = 0
    if file.is_dir:
        for sub_file in file.files:
            result += part_1(sub_file)
    else:
        return 0
    if file.size < s:
        return result + file.size
    return result


def part_2(file: File):
    dirs = []
    free_space = 70000000 - root.size
    required_size = 30000000 - free_space

    def _inner(file: File):
        if file.is_dir:
            if file.size >= required_size:
                dirs.append(file.size)
            for sub_file in file.files:
                _inner(sub_file)

    _inner(file)
    return sorted(dirs, reverse=False)[0]


with open("07_input.txt") as f:
    root = File(True, "/")
    current_dir = root
    raw_data = f.read().splitlines()
    current_line = -1
    while current_line < len(raw_data) - 1:
        current_line += 1
        line = raw_data[current_line]
        if line.startswith("$"):
            match line.replace("$ ", "").split(" "):
                case ["cd", dir_name]:
                    if dir_name == "/":
                        current_dir = root
                        continue
                    if dir_name == "..":
                        current_dir = current_dir.parent
                        continue
                    if existing_dir := list(
                        filter(lambda x: x.name == dir_name, current_dir.files)
                    ):
                        current_dir = existing_dir[0]
                        continue

                    new_dir = File(True, dir_name, parent=current_dir)
                    current_dir.files.append(new_dir)
                    current_dir = new_dir
                case ["ls"]:
                    current_line += 1
                    while current_line < len(raw_data) and not raw_data[
                        current_line
                    ].startswith("$"):
                        match raw_data[current_line].split(" "):
                            case ["dir", name]:
                                current_dir.files.append(
                                    File(True, name, parent=current_dir)
                                )
                            case [size, name]:
                                current_dir.files.append(
                                    File(False, name, size=int(size))
                                )

                        current_line += 1

                    current_line -= 1


root.size = calc_dir_size(root)
print("Part 1:", part_1(root))
print("Part 2:", part_2(root))
