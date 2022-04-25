# Rules

Riichi Mahjong has a wide range of rule variations. This project supports a few, but it is not exhaustive. For example, it does not support こやく

> These words can be found in a ruleset file. Ruleset files are `JSON` files. It supports UTF-8 encoding, so you do not have to use English.

| Variable | Variable Alias | Term | Values | Note |
| --- | --- | --- | --- | --- |
| `enableKuitan` | `食断` / `喰い断` | [Kuitan](https://riichi.wiki/Tanyao#Kuitan) | `true` / `false` |  |
| `enableAtozuke` | `后付` / `後付け` | [Atozuke](https://riichi.wiki/Atozuke) | `true` / `false` |  |
| `enableMultiRon` | `无截和` / `複数和了` | [Multiple ron](https://riichi.wiki/Multiple_ron) | `true` / `false` | Includes double-ron and triple-ron. |
| `enableIppatsu` | `一发` / `一発` | [Riichi Ippatsu](https://riichi.wiki/Ippatsu) | `true` / `false` | 
| `enableNoTenPenalty` | `未听罚符` / `ノーテン罰符` | [Noten Bappu](https://riichi.wiki/Bappu) | `true` / `false` |
| `enableBust` | `击飞` / `飛び` | [Tobi](https://riichi.wiki/End_game_scenarios#Tobi) | `true` / `false` | Whether games end when a player falls below zero points. |
| `minYaku` | `番缚` / `縛り` | [Shibari (JP)](https://ja.wikipedia.org/wiki/%E9%BA%BB%E9%9B%80%E3%81%AE%E3%83%AB%E3%83%BC%E3%83%AB#%E7%B8%9B%E3%82%8A) | `"0"` / `"1"` / `"2"` / `"4"` / `"mangan"` = `"满贯"` = `"満貫"` / `"yakuman"` = `"役满"` = `"役満"` |
| `redDora` | `红宝牌` / `赤ドラ` | [Akadora](https://riichi.wiki/Dora#Akadora) | `0` / `3` / `4` | 4 dora rule includes one more red dora `5p`. |
