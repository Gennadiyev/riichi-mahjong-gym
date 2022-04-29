'''
File: ruleset.py
Author: Kunologist
Description:
    Parses a rule file json to a format that could be used by the game environment.
'''

import json
import os
from unicodedata import name

key_mapping = {
    # Key aliases
    "食断": "enableKuitan",
    "喰い断": "enableKuitan",
    "后付": "enableAtozuke",
    "後付け": "enableAtozuke",
    "无截和": "enableMultiRon",
    "複数和了": "enableMultiRon",
    "一发": "enableIppatsu",
    "一発": "enableIppatsu",
    "未听罚符": "enableNoTenPenalty",
    "ノーテン罰符": "enableNoTenPenalty",
    "击飞": "enableBust",
    "飛び": "enableBust",
    "番缚": "minYaku",
    "縛り": "minYaku",
    "红宝牌": "redDora",
    "赤ドラ": "redDora"
}

deprecated_key_mapping = {
    # Undocumented aliases
    "akaDora": "redDora",
    "akadora": "redDora",
    "罚符": "enableNoTenPenalty"
}

min_yaku_mapping = {
    "满贯": "mangan",
    "満貫": "mangan",
    "役满": "yakuman",
    "役満": "yakuman"
}

default = {
    "enableKuitan": True,
    "enableAtozuke": True,
    "enableMultiRon": True,
    "enableIppatsu": True,
    "enableNoTenPenalty": True,
    "enableBust": True,
    "minYaku": "0",
    "redDora": 3
}


class Ruleset:
    '''
    Class: Ruleset

    ## Description
    
    This class is used to parse a ruleset json file to a format that could be
    used by the game environment. For ruleset configurations, check out the
    maj-soul example ruleset files and `rules.md` documentation page.
    '''
    
    rules = None
    name = None
    path = None

    def __init__(self, ruleset_path_or_string: str = None):
        '''
        Constructor: __init__

        ## Description

        This constructor takes a ruleset path or string and parses it to a
        format that could be used by the game environment.

        ## Parameters

        - `ruleset_path_or_string`: `str`
            The path to the ruleset json file or the ruleset json string.
            An input that ends with `.json` is considered a path.
        
        ## Details

        The ruleset json file must be a valid json dictionary. The translated
        keys are stored in the `rules` attribute.

        A ruleset json file may contain extra keys that are not used by the
        game. The extra values will be ignored. You will not see the extra
        keys after exporting the ruleset.

        ## Examples

        Parses the ruleset file at `rules/ruleset.json` and prints the name:

        ```python
        >>> ruleset = Ruleset('rules/ruleset.json')
        >>> print(ruleset.name)
        ```
        '''

        self.rules = default
        self.path = None
        self.name = "Default ruleset"
        if isinstance(ruleset_path_or_string, str) and ruleset_path_or_string.endswith('.json'):
            try:
                with open(ruleset_path_or_string, 'r') as ruleset_file:
                    ruleset = json.load(ruleset_file)
                    self.path = ruleset_path_or_string
            except FileNotFoundError:
                raise FileNotFoundError(f'Ruleset file not found: {ruleset_path_or_string}')
            except json.decoder.JSONDecodeError:
                raise json.decoder.JSONDecodeError(f'Ruleset file is not a valid json file: {ruleset_path_or_string}')
            except Exception as e:
                raise e
            self.__parse_ruleset(ruleset)
        elif isinstance(ruleset_path_or_string, str):
            try:
                ruleset = json.loads(ruleset_path_or_string)
            except json.decoder.JSONDecodeError:
                raise json.decoder.JSONDecodeError(f'Ruleset string is not a valid json string: {ruleset_path_or_string}')
            except Exception as e:
                raise e
            self.__parse_ruleset(ruleset)
        elif ruleset_path_or_string is None:
            pass
        else:
            raise TypeError("Invalid constructor type {}, expected str or None".format(type(ruleset_path_or_string)))
     
    def __parse_ruleset(self, ruleset: dict):
        '''
        Method: parse_ruleset

        ## Description

        Parses rules and name.

        This method parses the ruleset json file to a format that could be used
        by the game environment. This phase converts Kanji and non-ascii
        characters to ascii keys.

        For more information on how the keys are translated, visit `rules.md`
        in the documentation. 

        ## Parameters

        - `ruleset`: `dict`
            The ruleset json dictionary.
        '''

        # Check rules key
        if "rules" in ruleset:
            rules = ruleset["rules"]
        else:
            raise KeyError("Ruleset file does not contain a 'rules' key.")
        # Copy rules to prevent overwriting
        rules_copy = rules.copy()
        # Rules key mapping
        for key in rules_copy.keys():
            if key in key_mapping:
                rules[key_mapping[key]] = rules.pop(key)
            elif key in deprecated_key_mapping:
                rules[deprecated_key_mapping[key]] = rules.pop(key)
                print(f"[WARNING] The key '{key}' is deprecated and will be removed in the future. Please use `{deprecated_key_mapping[key]}` instead.")
        # minYaku mapping
        if "minYaku" in rules:
            if rules["minYaku"] in min_yaku_mapping:
                rules["minYaku"] = min_yaku_mapping[rules["minYaku"]]
        # Update rules
        self.rules.update(rules)

        # Set name
        if "name" in ruleset:
            self.name = ruleset["name"]
        else:
            self.name = "Untitled"

    def export(self, output_path: str):
        '''
        Method: export

        ## Description

        Exports the ruleset to a json file. Note that the ruleset name is
        exported as well, and the unexepected keys are ignored.

        ## Parameters

        - `output_path`: `str`
            The path to the output file.
        '''

        # Creates the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Exports the ruleset
        try:
            with open(output_path, 'w') as output_file:
                json.dump(
                    {
                        "rules": self.rules,
                        "name": self.name
                    }, output_file, indent=2
                )
        except FileNotFoundError:
            raise FileNotFoundError(f'Unable to create output ruleset file: {output_path}')
        except Exception as e:
            raise e

    def __str__(self):
        '''
        Method: __str__

        ## Description

        Returns a human

        ## Returns

        `str`
        '''

        o = "Ruleset {} ({})\n".format(self.name, self.path)
        for key in self.rules.keys():
            o += "  {}: {}\n".format(key, self.rules[key])
        return o
    
    def __repr__(self):
        '''
        Method: __repr__

        ## Description

        Returns the dataset string representation.

        ## Returns

        `str`
        '''
        return "Ruleset({})".format(self.path)
        
