# Class: `Action`

Action for the game of mahjong. This class is just for
representation, and does not contain any logic.

Some methods here have different parameters than others.
You may or may not use them, but an `Action` object should
usually be created using the oridinary constructor.

```python
from env.action import Action
```

---
 
# Constructor

## Description

The constructor of the `Action` class.

## Parameters

- `action_type`: `str`
    The type of the action.
- `action_string`: `str`
    The string representation of the action.

## Details

Here is the list of possible action types:

- `noop` (no operation)
- `akan`
- `mkan`
- `kan`
- `chii`
- `pon`
- `discard`
- `replace`
- `reach`
- `ron`
- `tsumo`
- `ten`
- `noten`

The action string notation is as follows:

### `akan`

Concealed quad (ankan, 暗槓).

E.g. `"121212a12"` (ankan of 2m)

The `"a"` is always placed before the 4-th tile.

### `mkan`

Exposed quad (minkan, 明槓).

E.g. `"121212m12"` (minkan of 2m)

The `"m"` is put where the tile is called. Placing
before the 3-rd tile means calling from the next player.

### `kan`

Late kan (kakan, 加槓).

E.g. `"47k474747"` (kakan of 7z)

The `"k"` is placed where the tile is previously called
pon. Placing before the 2-nd tile means that the tile
is previously pon-ed from the opposing player.

### `chii`

Call for sequence (chii, 吃).

E.g. `"c275226"` (chii of dora 7p with 5p and 6p in hand)

The `"c"` is always placed before the first tile since
we only chii from the previous player.

### `pon`

Call for pon (pon, 碰).

E.g. `"41p4141"` (pon of 1z)

The `"p"` is put before the called tile. Placing before
the 2-nd tile means that the tile is pon-ed from the
opposing player.

### `discard`

Discard (discard, 捨てる). Discards the incoming tile.

*(no action string)*

### `replace`

Cut (切る).

The action string should be the tile that is discarded.

E.g. `"41"` (cut 1z from hand)

### `reach`

Call reach (riichi, 立直).

The action string should be the tile that is discarded.
This action also calls reach.

E.g. `"r51"` (riichi with 0m)
`"r60"` (richii with discard)

### `ron`

Call ron (ron, ロン).

*(no action string)*

### `tsumo`

Call tsumo (tsumo, ツモ).

*(no action string)*

### `ten`

Call ten (tenpai, 聴牌), i.e. the player has a waiting
hand by the end of a game.

*(no action string)*

### `noten`

Call noten (noten, 不聴), i.e. the player does NOT
have a waiting hand by the end of a game.

*(no action string)*

# Method: `CHII`

## Description

This function returns a `CHII` action from the given
tile id and chii string.

## Parameters

- `chii_string`: `str`
    The string representation of the action.

## Returns

A `chii` action.

# Method: `PON`

## Description

This function returns a `PON` action from the given
pon string.

## Parameters

- `pon_string`: `str`
    The string representation of the action.

## Returns

A `pon` action.

# Method: `KAN`

## Description

This function returns a `KAN` action from the given
pon string.

## Parameters

- `pon_or_kan_string`: `str`
    The string representation of the pon / the string
    representation of the kan.

## Returns

A `kan` action.

# Method: `AKAN`
    
## Description

This function returns an `AKAN` action from the given
akan string.

## Parameters

- `tile_id`: `int` / `str`
    The id of the tile. Not `"4s"` string! The `str`
    input should be the string of an integer, e.g.
    `"13"`.

## Returns

An `akan` action.

# Method: `DISCARD`
        
## Description

This function returns a `DISCARD` action.

## Returns

A `discard` action.

# Method: `REPLACE`
        
## Description

This function returns a `REPLACE` action from the given
tile id.

## Parameters

- `tile_id`: `int`
    The id of the tile.

## Returns

A `replace` action.

# Method: `REACH`
        
## Description

This function returns a `REACH` action from the given
tile id.

## Parameters

- `tile_id`: `int`
    The id of the tile. If `tile_id` is `0` or `60`,
    the action means that the player calls reach upon
    discard

## Returns

A `reach` action.

# Method: `TSUMO`
        
## Description

This function returns a `TSUMO` action.

## Returns

A `tsumo` action.

# Method: `RON`

## Description

This function returns a `RON` action.

## Returns

A `ron` action.

# Method: `TEN`
        
## Description

This function returns a `TEN` action.

## Returns

A `ten` action.

# Method: `NOTEN`
        
## Description

This function returns a `NOTEN` action.

## Returns

A `noten` action.

# Method: `get_unicode_str`

## Description

This function returns the unicode string representation
of the action string.

## Returns

A `str` representing the unicode string.

## Examples

```python
>>> action = Action("chii", "c313233")
>>> print(action.get_unicode_str())    
chii c🀐🀑🀒
```
# Method: `get_tiles`

## Description

This function returns all tiles that are involved in the
action string.

## Returns

A `list` of `Tile` objects.

## Examples

```python
>>> action = Action("chii", "c313233")
>>> print(action.get_tiles())
[Tile(31), Tile(32), Tile(33)]
```

# Additional Methods

`Action` objects supports `__str__` and `__repr__`, `__hash__`, `__eq__` and `__ne__` methods.

- `__repr__` method returns `Action(action_type, action_string)`, which follows the rule `eval(Action.RON().__repr__()) == Tile(id)`.


