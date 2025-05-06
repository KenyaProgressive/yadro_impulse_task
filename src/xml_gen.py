import xml.dom.minidom as dom
import xml.etree.ElementTree as Et

def delete_prologue(minidom_xml_str):
    return b"\n".join([line for line in minidom_xml_str.split(b"\n") if line.strip() and not line.startswith(b"<?xml")])


def make_a_dict(keys: list, vals: list) -> dict:
    return dict(zip(keys, vals))

def xml_pretty_format(root: Et.Element):
    xml_str = Et.tostring(root)
    xml_dom = dom.parseString(xml_str)
    pretty_xml_str = delete_prologue(xml_dom.toprettyxml(encoding="utf-8"))
    with open("../out/config.xml", "wb") as cf:
        cf.write(pretty_xml_str)


def read_input_xml():
    class_configs: list = []
    class_names: list = []
    index: int = 0
    class_attrs: dict = dict()
    aggregations: list = []

    tree = Et.parse("../input/impulse_test_input.xml")
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

    for aggregation in root.findall("Aggregation"):
        aggregations.append({
            'source': aggregation.get("source"),
            'target': aggregation.get("target"),
            'sourceMultiplicity': aggregation.get("sourceMultiplicity"),
            'targetMultiplicity': aggregation.get("targetMultiplicity")
        })

    class_config_names_dict = make_a_dict(class_names, class_configs)

    print(class_config_names_dict)
    print(class_attrs)
    print(aggregations)

    return class_config_names_dict, class_attrs, aggregations


def do_xml_structure(current_elem, class_name, class_attrs, aggregations, checked_classes=None):
    if checked_classes is None:
        checked_classes = set()
    checked_classes.add(class_name)
    for attr in class_attrs.get(class_name, []):
        element = Et.SubElement(current_elem, attr["name"])
        element.text = attr["type"]
    for aggregation in aggregations:
        if aggregation["target"] == class_name:
            child_class_name = aggregation["source"]
            child_element = Et.SubElement(current_elem, child_class_name)
            do_xml_structure(child_element, child_class_name, class_attrs, aggregations, checked_classes)


def config_xml_create() -> None:
    class_config_names_dict, class_attrs, aggregations = read_input_xml()
    root_name: str = ""
    for class_name in class_config_names_dict:
        if class_config_names_dict[class_name]["isRoot"] == 'true':
            root_name = class_name
            break
    root = Et.Element(root_name)
    do_xml_structure(root, root_name, class_attrs, aggregations)
    xml_pretty_format(root)