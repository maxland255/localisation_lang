#  Copyright (c) 2024 pieteraerens.eu
#  All rights reserved.
#  The file lang_init.py is a part of localisation.
#  Created by harrypieteraerens
#  Created: 4/28/24, 2:16 AM
#  Last modified: 4/28/24, 2:16 AM

import json

from pathlib import Path
from datetime import datetime


class LangInit:
    def __init__(self, default_language: str = "en_us", reload_localization_on_launch: bool = False) -> None:
        """
        Initialisation of the language class

        :param default_language: Default language of the app
        :param reload_localization_on_launch: Reload the localization on launch program
        """
        self.__default_language = default_language
        self.__reload_localization_on_launch = reload_localization_on_launch

        self.__not_translated: dict[str, list[str]] = {}

        # Init the directories
        self.__local_dir = Path("./local")
        self.__localisation_dir = Path("./localisation")
        self.__untranslated_json = Path("./untranslated.json")

        # Init the project
        self.__init_project()

        # Get all language files
        self.__all_language_files = self.__get_all_lang_files()

        # Get all localizations
        self.__all_localization = self.__get_all_localization()

    def reload_localization(self) -> None:
        """
        Reload the localization files

        :return:
        """
        default_localization: Path = Path(self.__localisation_dir, f"{self.__default_language}.json")
        default_localization_data: dict[str, dict[str, dict[str]] | str] = json.load(default_localization.open(mode="rb"))

        translation_found: dict[str, list[str]] = {}

        for localization in self.__all_language_files:
            result = self.__write_localization_file(localization, default_localization_data)
            translation_found[localization.stem] = result

        self.__not_translated: dict[str, list[str]] = {}

        for key in default_localization_data.keys():
            if key.startswith("@"):
                continue
            for local in translation_found:
                if key not in translation_found[local]:
                    if self.__not_translated.get(local, None) is None:
                        self.__not_translated[local] = []
                    self.__not_translated[local].append(key)

        with self.__untranslated_json.open(mode="w") as file:
            file.write(json.dumps(self.__not_translated, indent=4))

        self.__write_master_localization_file(default_localization_data)

    def __init_project(self):
        """
        Init the project files

        :return:
        """
        if not self.__local_dir.exists():
            self.__local_dir.mkdir(exist_ok=True)

        if not self.__localisation_dir.exists():
            self.__localisation_dir.mkdir(exist_ok=True)

            default_language_file = Path(self.__localisation_dir, f"{self.__default_language}.json")
            default_language_file.touch(exist_ok=True)
            with default_language_file.open(mode="w") as file:
                file.write("{}")

        if not self.__untranslated_json.exists():
            self.__untranslated_json.touch(exist_ok=True)

            with self.__untranslated_json.open(mode="w") as file:
                file.write("{}")

    def __get_all_lang_files(self) -> list[Path]:
        """
        Get all language files

        :return: List of language files
        """

        return list(self.__localisation_dir.glob("*.json"))

    def __get_all_localization(self) -> list[str]:
        """
        Get all localization files

        :return: List of localization files
        """
        localization_found: list[str] = []

        for file in self.__all_language_files:
            localization_found.append(file.stem)

        return localization_found

    def __write_localization_file(self, localization: Path, default_localization: dict[str, dict[str, dict[str]] | str] | None = None) -> list[str]:
        """
        Write the localization file

        :return:
        """
        python = f"""\"\"\"
DO NOT MODIFY THIS FILE

This file is generated by the locallang Python Package.

Generated on {datetime.now().strftime("%m/%d/%y, %I:%M %p")}
Localisation: {localization.stem.capitalize()}
\"\"\"

from datetime import datetime, time
from typing import Any


class Localisation{localization.stem.capitalize()}:
    def __init__(self) -> None:
        pass
"""

        translation_found: list[str] = []

        with localization.open(mode="rb") as file:
            translations = json.load(file)

        if translations is None:
            raise ValueError("No translations found")

        for key, value in translations.items():
            if key.startswith("@"):
                continue

            translation_found.append(key)

            # Get the parameters
            parameters = translations.get(f"@{key}", None) or default_localization.get(f"@{key}", None)
            placeholders_found: list[str] = []

            parameters_str = ""
            parameters_check = ""
            parameters_to_str = ""

            # Define the return_translation
            return_translation = f"return f\"{value.replace('"', '\\"')}\""

            # Check if no_f_string is found
            no_f_string = parameters.get("no_f_string", False) if parameters is not None else False

            if no_f_string:
                return_translation = f"return \"{value.replace('"', '\\"')}\""

            if parameters is not None:
                # Check if placeholders are found in the translation
                placeholders = parameters.get("placeholders", None)
                if placeholders is not None:
                    for placeholder, data in placeholders.items():
                        placeholders_found.append(placeholder)

                        placeholder_type = data.get("type", None)

                        # Check if placeholder_type is supported
                        if placeholder_type not in ["int", "float", "str", "bool", "datetime", "time"]:
                            raise ValueError(f"Type {placeholder_type} is not supported")

                        # Check if placeholder name is a reserved keyword
                        if placeholder in ["self", "cls", "int", "float", "str", "bool", "datetime", "time"]:
                            raise ValueError(f"{placeholder} is a reserved keyword")

                        # Check if placeholder_type is datetime or time
                        if placeholder_type in ["datetime", "time"]:
                            date_format = data.get("format", None)
                            if date_format is None:
                                raise ValueError("No date format found")

                            # Add the placeholder to the parameters_str
                            parameters_str += f", {placeholder}: {placeholder_type}"

                            # Add the placeholder to the parameters_check
                            parameters_check += f"        assert isinstance({placeholder}, {placeholder_type}), f\"{placeholder} must be a {placeholder_type}\"\n"

                            # Add the placeholder to the parameters_to_str
                            parameters_to_str += f"        {placeholder} = {placeholder}.strftime('{date_format}')\n"

                            if no_f_string:
                                # Add the placeholder to the return_translation
                                return_translation += f".replace('{{{placeholder}}}', {placeholder})"
                            continue

                        # Add the placeholder to the parameters_str
                        parameters_str += f", {placeholder}: {placeholder_type}"

                        # Add the placeholder to the parameters_check
                        parameters_check += f"        assert isinstance({placeholder}, {placeholder_type}), f\"{placeholder} must be a {placeholder_type}\"\n"

            # Check if placeholders are found directly in the translation
            for translation in value.split(" "):
                if translation.startswith("{") and translation.endswith("}"):
                    placeholder = translation[1:-1]
                    if placeholder not in placeholders_found:
                        # Add the placeholder to the parameters_str
                        parameters_str += f", {placeholder}: Any"

                        if no_f_string:
                            # Add the placeholder to the return_translation
                            return_translation += f".replace('{{{placeholder}}}', {placeholder})"

            localization_function = f"""
    def {key.lower().replace(" ", "_")}(self{parameters_str}) -> str:
{parameters_check}{parameters_to_str}
        {return_translation}
"""
            python += localization_function

        with Path(self.__local_dir, f"{localization.stem}.py").open(mode="w") as file:
            file.write(python)

        return translation_found

    def __write_master_localization_file(self, default_localization: dict[str, dict[str, dict[str]] | str] | None = None) -> None:
        """
        Write the localization file

        :return:
        """
        from_localization = ""

        for local in self.__all_localization:
            from_localization += f"from .{local} import Localisation{local.capitalize()}\n"

        python = f"""\"\"\"
DO NOT MODIFY THIS FILE

This file is generated by the locallang Python Package.

Generated on {datetime.now().strftime("%m/%d/%y, %I:%M %p")}
Localisation: Master Localisation
\"\"\"

from datetime import datetime, time
from typing import Any
{from_localization}

class Localisation:
    def __init__(self, local: str) -> None:
        self.__local = local
"""

        translation_found: list[str] = []

        for key, value in default_localization.items():
            if key.startswith("@"):
                continue

            translation_found.append(key)

            # Get the parameters
            parameters = default_localization.get(f"@{key}", None)
            placeholders_found: list[str] = []

            parameters_str = ""
            parameters_check = ""
            parameters_call_str = ""

            if parameters is not None:
                placeholders = parameters.get("placeholders", None)
                if placeholders is not None:
                    for placeholder, data in placeholders.items():
                        placeholders_found.append(placeholder)

                        placeholder_type = data.get("type", None)

                        # Check if placeholder_type is supported
                        if placeholder_type not in ["int", "float", "str", "bool", "datetime", "time"]:
                            raise ValueError(f"Type {placeholder_type} is not supported")

                        # Add the placeholder to the parameters_str
                        parameters_str += f", {placeholder}: {placeholder_type}"

                        # Add the placeholder to the parameters_check
                        parameters_check += f"        assert isinstance({placeholder}, {placeholder_type}), f\"{placeholder} must be a {placeholder_type}\"\n"

                        # Add the placeholder to the parameters_call_str
                        parameters_call_str += f", {placeholder}={placeholder}" if parameters_call_str != "" else f"{placeholder}={placeholder}"

            # Check if placeholders are found directly in the translation
            for translation in value.split(" "):
                if translation.startswith("{") and translation.endswith("}"):
                    placeholder = translation[1:-1]
                    if placeholder not in placeholders_found:
                        # Add the placeholder to the parameters_str
                        parameters_str += f", {placeholder}: Any"

                        # Add the placeholder to the parameters_call_str
                        parameters_call_str += f", {placeholder}={placeholder}" if parameters_call_str != "" else f"{placeholder}={placeholder}"

            # Define the return_translation
            return_translation = ""

            for local in self.__all_localization:
                if self.__not_translated.get(local, None) is not None and key in self.__not_translated.get(local, []):
                    return_translation += f"""
        if self.__local == \"{local}\":
            raise ValueError(\"{key} is not translated in {local}\")
"""

                else:
                    return_translation += f"""
        if self.__local == \"{local}\":
            return Localisation{local.capitalize()}().{key.lower().replace(" ", "_")}({parameters_call_str})
"""

            return_translation += "        return None"

            localization_function = f"""
    def {key.lower().replace(" ", "_")}(self{parameters_str}) -> str | None:
{parameters_check}{return_translation}
"""
            python += localization_function

        with Path(self.__local_dir, "localisation.py").open(mode="w") as file:
            file.write(python)
