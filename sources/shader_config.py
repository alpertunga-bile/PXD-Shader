from os import getcwd
from os.path import join, exists
from re import findall, sub
from typing import Tuple
from json import dump, loads


def get_imports(shader: str) -> dict[str, Tuple[str, str]]:
    imports = {}

    import_substrings = findall("from\s+", shader)
    start_pos = 0

    for substring in import_substrings:
        start_index = shader.find(substring, start_pos)
        eol_index = shader.find("\n", start_index)

        import_strings = shader[start_index:eol_index].split(" ")
        import_from = import_strings[1]
        import_thing = sub(
            r"[^a-zA-Z0-9_-]*", "", import_strings[3]
        )  # can put semicolon at the end for not break the formatting program
        imports[import_thing] = (import_from, shader[start_index:eol_index])

        start_pos = eol_index

    return imports


def get_wanted_string(file_string: str, name: str) -> str:
    regex = f"[()a-zA-Z0-9,=\s]*{name}[()a-zA-Z0-9,.=\s]*\n*"
    regex += "{?;?"

    name_syntax = findall(regex, file_string)

    if len(name_syntax) == 0:
        return ""

    start_index = file_string.find(name_syntax[0])

    if file_string.find("};", start_index) != -1:
        end_index = file_string.find("};", start_index) + 2
    elif file_string.find("}", start_index) != -1:
        end_index = file_string.find("}", start_index) + 1
    elif file_string.find(";", start_index) != -1:
        end_index = file_string.find(";", start_index) + 1

    return file_string[start_index:end_index]


def import_externals(shader: str) -> str:
    imports = get_imports(shader)
    modified_shader = shader

    for thing, (file, thing_info) in imports.items():
        shader_file = join("shaders", file)

        if exists(shader_file) is False:
            print(f"{shader_file} is not exists so {thing} can't be imported")
            continue

        with open(shader_file, "r") as import_file:
            import_string = import_file.read()

        wanted_thing = get_wanted_string(import_string, thing)

        modified_shader = modified_shader.replace(thing_info, wanted_thing)

    return modified_shader


def get_extensions(shader: str) -> dict[str, str]:
    extensions = {}
    start_pos = 0

    extension_substrings = findall("#extension", shader)

    for substring in extension_substrings:
        start_index = shader.find(substring, start_pos)
        eol_index = shader.find("\n", start_index)

        # expected syntax:
        # #extension [extension_name] : [extension_status]
        extension_strings = shader[start_index:eol_index].split(" ")
        extension_name = extension_strings[1]
        extension_status = extension_strings[3]
        extensions[extension_name] = extension_status

        start_pos = eol_index  # look for other extensons as the starting point from the new line

    return extensions


if __name__ == "__main__":
    print(f"Working Directory : {getcwd()}")

    shader_filename = join("shaders", "model.vert")

    with open(shader_filename, "r") as shader_file:
        shader = shader_file.read()

    shader_infos = {}
    extensions = get_extensions(shader)

    shader_infos["extensions"] = extensions

    print(shader_infos)

    shader = import_externals(shader)

    print(shader)

    with open(shader_filename + ".json", "w") as json_file:
        dump(shader_infos, json_file, indent=4)

    with open(shader_filename + ".json", "r") as json_file:
        json = loads(json_file.read())
        print(json["extensions"]["GL_NV_command_list"])
