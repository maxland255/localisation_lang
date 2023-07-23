import json
import os
import re
from typing import Any

try:
    from local.localisation import Localisation
except:
    print("\n\nPlease restart the app to finish the initialisation !\n\n")

startPrefix = "{"
endPrefix = "}"

class LangInit:
    __default_app_lang: str | None = None

    def __init__(self, default_app_lang: str = "en_us", reload_localisation: bool = True) -> None:
        file_path_exist = os.path.exists("./local/localisation.py")
        default_lang_path_exist = os.path.exists(f"./localisation/{default_app_lang}.json")
        self.__default_app_lang = default_app_lang

        if file_path_exist == False:
            os.makedirs("./local", exist_ok=True)
            file = open("./local/localisation.py", "w")
            file.write("import json\nfrom datetime import datetime, time\nclass Localisation:\n\t__lang: str\n\tdef __init__(self, lang: str) -> None:\n\t\tself.__lang = lang\n\tdef __get_local_str(self, key: str) -> str | None:\n\t\ttry:\n\t\t\tlang_file = open(f\"./local/{self.__lang}.json\", \"rb\")\n\t\t\tlang_js: dict[str, str] = json.loads(lang_file.read())\n\t\t\tlang_file.close()\n\t\t\treturn lang_js.get(key)\n\t\texcept:\n\t\t\tprint(f\"\\n\\nLocalisation {self.__lang} is not supported\\n\\n\")\n\t\t\treturn None")
            file.close()
        
        if default_lang_path_exist == False:
            os.makedirs("./localisation", exist_ok=True)
            file = open(f"./localisation/{default_app_lang}.json", "w")
            file.write("{}")
            file.close()
        
        if file_path_exist == False or default_lang_path_exist == False:
            exit(0)
        
        if reload_localisation:
            self.reload_localisation()

    def reload_localisation(self):
        lang_files = os.listdir("./localisation")

        for l in lang_files:
            if l.endswith(".json"):
                l = l.removesuffix(".json")
                local_json_file = open(f"./localisation/{l}.json", "rb")
                json_lang: dict[str, str] = json.loads(local_json_file.read())
                local_json_file.close()

                new_local_json_file = open(f"./local/{l}.json", "w")
                new_local_json_file.write(json.dumps(json_lang))
                new_local_json_file.close()
                        
        default_local_json_file = open(f"./localisation/{self.__default_app_lang}.json", "rb")
        default_json_lang: dict[str, str | Any] = json.loads(default_local_json_file.read())
        default_local_json_file.close()

        local_py_file = open("./local/localisation.py", "w")

        python_lang = "import json\nfrom datetime import datetime, time\nclass Localisation:\n\t__lang: str\n\tdef __init__(self, lang: str) -> None:\n\t\tself.__lang = lang\n\tdef __get_local_str(self, key: str) -> str | None:\n\t\ttry:\n\t\t\tlang_file = open(f\"./local/{self.__lang}.json\", \"rb\")\n\t\t\tlang_js: dict[str, str] = json.loads(lang_file.read())\n\t\t\tlang_file.close()\n\t\t\treturn lang_js.get(key)\n\t\texcept:\n\t\t\tprint(f\"\\n\\nLocalisation {self.__lang} is not supported\\n\\n\")\n\t\t\treturn None"

        if len(default_json_lang.keys()) > 0:
            for k in default_json_lang.keys():
                if k.startswith("@") == False:
                    value = default_json_lang.get(k)
                    key = k.replace(" ", "_")

                    param: dict[str, str] = default_json_lang.get(f"@{k}")

                    parameters = ""
                    replaceFunc = ""
                    condition = ""
                    usedParam: list[str]= []

                    if param != None:
                        placeholders: dict[str, str] = param.get("placeholders")
                        
                        pkeys = placeholders.keys()

                        for pk in pkeys:
                            usedParam.append(pk)
                            type = placeholders[pk].get("type")
                            if type != None:
                                if type == "int" or type == "float" or type == "str" or type == "bool":
                                    parameters += f", {pk}: {type}"
                                    convertStr = ""
                                    if type == "int" or type == "float" or type == "bool":
                                        convertStr = ".__str__()"
                                    replaceFunc += f".replace(\"{startPrefix}{pk}{endPrefix}\", {pk}{convertStr})"
                                elif type == "datetime" or type == "time":
                                    format = placeholders[pk].get("format")
                                    if format != None:
                                        parameters += f", {pk}: {type}"
                                        replaceFunc += f".replace(\"{startPrefix}{pk}{endPrefix}\", {pk}.strftime('{format}'))"
                                    else:
                                        print(f"`format` key is required for `datetime` or `time` type")
                                        exit(0)
                                else:
                                    print(f"`{type}` is not a supported type")
                                    exit(0)
                            else:
                                parameters += f", {pk}: str | int | float | bool | datetime | time"
                                condition += f"\n\t\tif type({pk}) == int or type({pk}) == float or type({pk}) == datetime or type({pk}) == time or type({pk}) == bool:\n\t\t\ttrad = trad.replace(\"{startPrefix}{pk}{endPrefix}\", {pk}.__str__())\n\t\telif type({pk}) == str:\n\t\t\ttrad = trad.replace(\"{startPrefix}{pk}{endPrefix}\", {pk})\n\t\telse:\n\t\t\tprint(f\"`{startPrefix}type({pk}){endPrefix}` is not a supported variable type\")\n\t\t\treturn None"

                    allKey: list[str] = re.findall("({[a-zA-Z]*})", value)

                    for a in allKey:
                        a = a.replace("{", "").replace("}", "")
                        if usedParam.__contains__(a) == False:
                            parameters += f", {a}: str | int | float | bool | datetime | time"
                            condition += f"\n\t\tif type({a}) == int or type({a}) == float or type({a}) == datetime or type({a}) == time or type({a}) == bool:\n\t\t\ttrad = trad.replace(\"{startPrefix}{a}{endPrefix}\", {a}.__str__())\n\t\telif type({a}) == str:\n\t\t\ttrad = trad.replace(\"{startPrefix}{a}{endPrefix}\", {a})\n\t\telse:\n\t\t\tprint(f\"`{startPrefix}type({a}){endPrefix}` is not a supported variable type\")\n\t\t\treturn None"
                    
                    if replaceFunc != "":
                        condition += f"\n\t\tif trad != None:\n\t\t\ttrad = trad{replaceFunc}"

                    python_lang += f"\n\tdef {key}(self{parameters}):\n\t\t\"\"\"In {self.__default_app_lang} this message is translate to: ``{value}``\n\t\t\"\"\"\n\t\ttrad = self.__get_local_str(\"{key}\"){condition}\n\t\treturn trad"

        local_py_file.write(python_lang)
        local_py_file.close()

    def getLocalisation(self, lang: str):
        if os.path.exists("./local/localisation.py"):
            try:
                return Localisation(lang=lang)
            except:
                return None
        else:
            return None