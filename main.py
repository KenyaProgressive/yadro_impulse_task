import xml.etree.ElementTree as Et


def read_input_xml() -> dict:
    xml_read_result = dict()
    tree: Et = Et.parse("input/impulse_test_input.xml")
    root = tree.getroot()
    return xml_read_result

def config_xml_create() -> None:
    bts = Et.Element("BTS")
    bts_id = Et.SubElement(bts, "id")
    bts_name = Et.SubElement(bts, "name")
    new_tree = Et.ElementTree(bts)
    new_tree.write("config.xml", encoding="utf-8")


def test() -> bool:
    success_flag: bool = True
    try:
        print(read_input_xml())
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
