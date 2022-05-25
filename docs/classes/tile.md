# Class: `Tile`

A `Tile` object represents a Mahjong tile.

```python
from env.tiles import Tile
```

## Description

This class is used to represent a single tile in the mahjong game.

## Details

The ID of the card is used to represent the card object. The mapping
between the ID and the card object is as follows:

- `11` ~ `19`: 1~9 man
- `21` ~ `29`: 1~9 pin
- `31` ~ `39`: 1~9 sou
- `41` ~ `47`: ton, nan, shaa, pei, haku, hatsu, chun
- `51` ~ `53`: Red dora 5 man, 5 pin, 5 sou

> The format follows the [tenhou.net](https://tenhou.net) configurations.

---

# Constructor

## Description

Creates a tile object from a tile object, a string, or an integer.

## Parameters

- `constructor`: `Tile` or `str` or `int`

## Details

If the constructor is a `Tile` object, the `Tile` object is copied.

If the constructor is a string, the tile object is created from the
string. Specify the rank, then the suit, without spaces:

- `"1m"` ~ `"9m"`: 1~9 man
- `"1p"` ~ `"9p"`: 1~9 pin
- `"1s"` ~ `"9s"`: 1~9 sou
- `"1z"` ~ `"7z"`: ton, nan, shaa, pei, haku, hatsu, chun
- `"0m"`, `"0p"`, `"0s"`: Red dora 5 man, 5 pin, 5 sou

If the constructor is an integer, the tile object is created from the
number.

- `11` ~ `19`: 1~9 man
- `21` ~ `29`: 1~9 pin
- `31` ~ `39`: 1~9 sou
- `41` ~ `47`: ton, nan, shaa, pei, haku, hatsu, chun
- `51` ~ `53`: Red dora 5 man, 5 pin, 5 sou

## Examples

```python
>>> tile_1m = tile('1m') # 1 man
>>> tile_3p = tile(41) # East
>>> tile_r5s = tile('0s') # Aka dora 5 sou
```

# Method: `get_id`

## Description

Returns the ID of the tile.

## Returns

- `int`: ID of the tile

# Method: `get_rank`

## Description

Returns the rank of the tile.

## Returns

- `int`: rank of the tile

## Examples

```python
>>> tile_0m = Tile("0m")
>>> tile_0m.get_rank()
5
```

# Method: `get_suit`

## Description

Returns the suit of the tile. If the tile is invalid, returns an
empty string. Otherwise, returns "m", "p", "s" or "z".

Note that there will be no special treatment for red dora. Use
`tile.is_red_dora()` instead.

## Returns

- `str`: suit of the tile

## Examples

```python
>>> tile_0m = Tile("0m")
>>> tile_0m.get_suit() 
'm'
```

# Method: `get_name`

## Description

Returns the name of the tile. Name is a string of the rank and suit,
e.g. `"1m"`, `"2p"`, `"0s"`, `"2z"`.

## Returns

- `str`: name of the tile

# Method: `get_136_id`

## Description

Returns the ID of the tile in 136-tile format. **This should not be
used because it is not guaranteed to be unique. A 136-tile ID is
only meaningful in a deck's context.**

## Returns

- `int`: ID of the tile in 136-tile format

## Details

This function will return a number in range [0, 135].

The mapping is as follows:

- 0~3: 1m
- 4~7: 2m
- 8~11: 3m
...
- 32~35: 9m
- 36~39: 1p
- 40~43: 2p
...
- 68~71: 9p
- 72~75: 1s
...
- 104~107: 9s
- 108~111: 1z
...
- 132~135: 7z

The aka dora will always be the first one in the four tiles:

- 16: 0m
- 52: 0p
- 88: 0s

Therefore `Tile("5m").get_136_id()` will return `17` instead of `16`.

# Method: `get_34_id`

## Description

Returns the ID of the tile in 34-tile format.

## Returns

- `int`: ID of the tile in 34-tile format

## Details

This function will return a number in range [0, 33].

The mapping is as follows:

- 0~8: 1~9m
- 9~17: 1~9p
- 18~26: 1~9s
- 27~33: 1~7z

Note that there will be no special treatment for red dora.

# Method: `get_unicode_tile`

## Description

Returns the unicode representation of the tile.

```python
man_tiles = ["🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"]
pin_tiles = ["🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"]
sou_tiles = ["🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"]
char_tiles = ["🀀", "🀁", "🀂", "🀃", "🀆", "🀅", "🀄"]
```

## Returns

- `str`: unicode representation of the tile

Note that a special empty tile `Tile()` will give an empty
string `""`. For invalid tile ID, the function will
return `"?"`.

# Method: `is_red_dora`

## Description

Returns whether the tile is red dora.

## Returns

- `bool`: whether the tile is red dora

# Method: `copy`

## Description

Returns a copy of the tile.

## Returns

- `tile`: copy of the tile

# Additional Methods

`Tile` class supports `__eq__`, `__ne__`, `__lt__`, `__le__`,
`__gt__`, `__ge__`, `__hash__`, `__str__`, `__repr__`.

- The comparator methods compares the ID of the tile.
- Each `Tile` will have a `hidden_id` attribute, used in `__hash__`.
- `__repr__` method returns `Tile(id)`, which follows the rule `eval(Tile(id).__repr__()) == Tile(id)`.
