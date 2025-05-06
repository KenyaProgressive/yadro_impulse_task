import xml.etree.ElementTree as Et

from xml_gen import config_xml_create


def launch() -> bool:
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
    if launch():
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
