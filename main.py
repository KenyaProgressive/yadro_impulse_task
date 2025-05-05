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
        index += 1
    # class_config_names_dict = dict(zip(class_names, ))

    for params_dict in


    print(class_configs)
    print(class_names)
    # return xml_read_result


def config_xml_create() -> None:
    bts = Et.Element("BTS")
    bts_id = Et.SubElement(bts, "id")
    bts_name = Et.SubElement(bts, "name")
    new_tree = Et.ElementTree(bts)
    new_tree.write("config.xml", encoding="utf-8")


def test() -> bool:
    success_flag: bool = True
    try:
        read_input_xml()
        # config_xml_create()
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
