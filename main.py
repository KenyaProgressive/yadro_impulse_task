import xml.etree.ElementTree as Et


def make_a_dict(keys: list, vals: list):
    return dict(zip(keys, vals))


def read_input_xml():
    class_configs: list = []
    class_names: list = []
    index: int = 0
    class_attrs = dict()

    tree = Et.parse("input/impulse_test_input.xml")
    root = tree.getroot()

    for tag in root.findall("Class"):
        tag_attrs = tag.attrib
        class_configs.append(tag_attrs)
        if "name" in tag_attrs:
            class_names.append(class_configs[index]["name"])

        class_configs[index].pop("name")

        class_attrs[class_names[index]] = []

        for attr in tag.findall("Attribute"):
            class_attrs[class_names[index]].append(attr.attrib)
        index += 1

    class_config_names_dict = make_a_dict(class_names, class_configs)

    print(class_config_names_dict)
    print(class_attrs)
    return class_config_names_dict, class_attrs


def config_xml_create() -> None:
    class_config_names_dict, class_attrs = read_input_xml()
    root_name = ""
    for class_name in class_config_names_dict:
        if class_config_names_dict[class_name]["isRoot"] == 'true':
            root_name = class_name
            break
    root = Et.Element(root_name)
    for attr in class_attrs.get(root_name, []):
        element_name = Et.SubElement(root, attr["name"])
        element_name.text = attr["type"]

    new_tree = Et.ElementTree(root)
    new_tree.write("config.xml", encoding="utf-8")


def test() -> bool:
    success_flag: bool = True
    try:
        config_xml_create()
    except FileNotFoundError:
        success_flag = False
        print("Файл не существует")
    except Et.ParseError as e:
        success_flag = False
        print(f"Парсинг XML не удался: {e}")
    return success_flag


def main() -> int:
    if test():
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
