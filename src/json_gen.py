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

        is_root = class_config_names_dict[class_name]["isRoot"].upper() == "TRUE"

        class_data = {"class": class_name,
                      "documentation": class_config_names_dict[class_name]["documentation"],
                      "isRoot": is_root,
                      "max": "0",
                      "min": "0",
                      "parameters": class_attrs[class_name]
                      }
        mini_values = []
        maxi_values = []

        if class_name in source_multiplicity:
            maxi_values.extend([i["max"] for i in source_multiplicity[class_name]])
            mini_values.extend([i["min"] for i in source_multiplicity[class_name]])
        elif class_name in target_multiplicity:
            maxi_values.extend([i["max"] for i in target_multiplicity[class_name]])
            mini_values.extend([i["min"] for i in target_multiplicity[class_name]])

        if mini_values and maxi_values:
            class_data["max"] = max(maxi_values, key=lambda x: int(x))
            class_data["min"] = min(mini_values, key=lambda x: int(x))

        if class_name in aggregation_parametres:
            class_data["parameters"].extend(aggregation_parametres[class_name])

        result.append(class_data)

        if is_root:
            class_data.pop("min")
            class_data.pop("max")

    with open("../out/meta.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)



def delta_json_generate():
    with open("../input/config.json", "r", encoding="utf-8") as cf:
        config_json = json.load(cf)
    with open("../input/patched_config.json", "r", encoding="utf-8") as pcf:
        patched_config_json = json.load(pcf)

    config_json_keys =  set(config_json.keys())
    patched_config_json_keys = set(patched_config_json.keys())

    additions = [{"key": key, "value": patched_config_json[key]} for key in sorted(patched_config_json_keys - config_json_keys)]
    deletions = sorted(config_json_keys - patched_config_json_keys)

    updates = []
    common_keys = config_json_keys & patched_config_json_keys
    for key in sorted(common_keys):
        if config_json[key] != patched_config_json[key]:
            updated = {"key": key, "from": config_json[key], "to": patched_config_json[key]}
            updates.append(updated)

    delta_json = {"additions": additions, "deletions": deletions, "updates": updates}
    with open("../out/delta.json", "w", encoding="utf-8") as f:
        json.dump(delta_json, f, indent=4)

def gen_result_of_patch_jsons():
    with open("../input/config.json", "r", encoding="utf-8") as cf:
        config_json = json.load(cf)
    with open("../out/delta.json", "r", encoding="utf-8") as df:
        delta_json = json.load(df)

    patched_conf = dict(config_json)
    for key in delta_json["deletions"]:
        if key in patched_conf:
            del patched_conf[key]

    for dictt in delta_json["updates"]:
        key = dictt["key"]
        if key in patched_conf:
            patched_conf[key] = dictt["to"]

    for dictt in delta_json["additions"]:
        patched_conf[dictt["key"]] = dictt["value"]

    with open("../out/res_patched_config.json", "w", encoding="utf-8") as f:
        json.dump(patched_conf, f, indent=4)