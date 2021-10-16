import sys
import json

TYPES_MAP = {
    'str': 'String',
    'int': 'Integer',
    'float': 'Float',
    'list': 'ArrayList'
}

PROGRAM_STRING = """class Programa {
   public static void main (String args[]){
   }
}"""


def generate_code(file):
    classes = parse_json(file)
    for klass in classes["classes"]:
        print(f"class {klass['name']} {{")
        for attr in klass["attributes"]:
            print(f"    {get_class_type(attr)} {attr[0]};")
        print("}\n")

    print(PROGRAM_STRING)


def get_class_type(attribute):
    type_ = attribute[1].__name__
    if type_ == 'dict':
        return attribute[0].capitalize()
    if type_ == 'list':
        return f"ArrayList<{attribute[0].capitalize()}>"
    return TYPES_MAP.get(attribute[0], 'String')


def parse_json(file):
    model = json.loads(file.read())
    classes = {"classes": []}

    def dict_recursion(d):
        keys = set(d.keys())
        for key in keys:
            if isinstance(d[key], dict):
                klass = {
                    "name": key,
                    "attributes": [(k, type(v)) for k, v in d[key].items()]
                }
                classes["classes"].append(klass)

                dict_recursion(d[key])

            if isinstance(d[key], list):
                klass = {
                    "name": key,
                    "attributes": [(k, type(v)) for k, v in d[key][0].items()]
                }
                classes["classes"].append(klass)

                dict_recursion(d[key][0])

    dict_recursion(model)
    return classes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: $ python3 javagen.py <json_file_to_parse>")
        sys.exit()

    file_path = sys.argv[1]

    with open(file_path, 'r') as f:
        generate_code(f)
