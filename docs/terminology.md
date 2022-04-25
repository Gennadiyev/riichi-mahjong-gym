# Terminology

Riichi Mahjong originates from the Japanese Mahjong game. Most of the terms are not native English words. Here is the list of the terms we use in the project.

This page also contains the variable naming convention of the project. So if you're not familiar with Japanese, you can check the table here.

## Tiles

### `sou`, "索"

🀐🀑🀒🀓🀔🀕🀖🀗🀘

### `pin`, "饼"

🀙🀚🀛🀜🀝🀞🀟🀠🀡

### `man`, "万"

🀇🀈🀉🀊🀋🀌🀍🀎🀏

## Rules

> These words can be found in a ruleset file. Ruleset files are `JSON` files. It supports UTF-8 encoding, so you do not have to use English.

| Variable | Variable Alias | Term | Values | Note |
| --- | --- | --- | --- | --- |
| `kuitan` | `食断` / `喰い断` | [Kuitan](https://riichi.wiki/Tanyao#Kuitan) | `true` / `false` |  |
| `atozuke` | `后付` / `後付け` | [Atozuke](https://riichi.wiki/Atozuke) | `true` / `false` |  |
| `multiRon` | `无截和` / `複数和了` | [Multiple ron](https://riichi.wiki/Multiple_ron) | `true` / `false` | Includes double-ron and triple-ron. |
| `ippatsu` | `一发` / `一発` | [Riichi Ippatsu](https://riichi.wiki/Ippatsu) | `true` / `false` | 
| `bappu` | `未听罚符` / `ノーテン罰符` | [Noten Bappu](https://riichi.wiki/Bappu) | `true` / `false` |
| `shibari` | `番缚` / `縛り` | [Shibari (JP)](https://ja.wikipedia.org/wiki/%E9%BA%BB%E9%9B%80%E3%81%AE%E3%83%AB%E3%83%BC%E3%83%AB#%E7%B8%9B%E3%82%8A) | `"0"` / `"1"` / `"2"` / `"4"` / `"mangan"` = `"满贯"` = `"満貫"` / `"yakuman"` = `"役满"` = `"役満"` |
| `akaDora` | `红宝牌` / `赤ドラ` | [Akadora](https://riichi.wiki/Dora#Akadora) | `0` / `3` / `4` | 4 dora includes one more red `5p`. |

