import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.ruleset import Ruleset

def test_ruleset_load():
    ruleset = Ruleset("rules/ruleset.json")
    assert ruleset
    assert ruleset.rules
    assert ruleset.rules["enableAtozuke"]

def test_default_ruleset():
    ruleset = Ruleset()
    assert ruleset
    assert ruleset.rules["enableAtozuke"] == True
    assert ruleset.rules["redDora"] == 3
    assert ruleset.name == "Default ruleset"

def test_translated_ruleset():
    ruleset = Ruleset('''{
  "name": "Translated Ruleset",
  "rules": {
    "食断": true,
    "后付": true,
    "enableMultiRon": false,
    "一发": false,
    "enableNoTenPenalty": false,
    "飛び": true,
    "縛り": "満貫",
    "红宝牌": 4
  }
}
''')
    assert ruleset
    assert ruleset.rules["enableAtozuke"] == True
    assert ruleset.rules["redDora"] == 4
    assert ruleset.rules["enableMultiRon"] == False
    assert ruleset.rules["enableIppatsu"] == False
    assert ruleset.name == "Translated Ruleset"
