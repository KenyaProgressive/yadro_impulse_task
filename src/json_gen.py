import json

from xml_gen import read_input_xml


def make_aggregations_dict(aggregations):
    aggregations_dict = {}
    source_multiplicity = {}
    target_multiplicity = {}

    for aggregation in aggregations:
        source = aggregation["source"]
        target = aggregation["target"]

        aggregation_parametres = {"name": source, "type": "class"}
        aggregations_dict.setdefault(target, []).append(aggregation_parametres)

        source_multiplicity_borders = aggregation["sourceMultiplicity"].split("..")
        s_min = source_multiplicity_borders[0]
        s_max = source_multiplicity_borders[-1]

        source_multiplicity_parametres = {"min": s_min, "max": s_max}
        source_multiplicity.setdefault(source, []).append(source_multiplicity_parametres)

    return aggregations_dict, source_multiplicity, target_multiplicity


def json_input():
    class_config_names_dict, class_attrs, aggregations = read_input_xml()

    aggregation_parametres, source_multiplicity, target_multiplicity = make_aggregations_dict(aggregations)

    result = []
    for class_name in class_config_names_dict:
        class_data = {"class": class_name,
                      "documentation": class_config_names_dict[class_name]["documentation"],
                      "isRoot": class_config_names_dict[class_name]["isRoot"].upper() == "TRUE",
                      "parameters": class_attrs[class_name]
                      }
        mini_values = []
        maxi_values = []


        if class_name in aggregation_parametres:
            class_data["parameters"].extend(aggregation_parametres[class_name])

    json_str = json.dumps(class_config_names_dict, indent=4)
    with open("../out/meta.json", "w", encoding="utf-8") as f:
        f.write(json_str)


json_input()
