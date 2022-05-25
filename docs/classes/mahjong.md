# Class: `MahjongGame`

A `MahjongGame` class where a `Mahjong` game takes place.

```python
from env.mahjong import MahjongGame, MahjongEndGame
```

The logic of riichi Mahjong is very complicated. There are many
game-ending scenarios, therefore as soon as the game finishes, 
an exception will be raised.

```python
class MahjongEndGame(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return "MahjongEndGame: {}".format(self.message)
```

Make sure to catch the exception as you train your agents:

```python
game = MahjongGame()
try:
    game.play()
except MahjongEndGame as e:
    print("Game finished!")
    print(game.get_state()["end_game"])
```

---

# Function: `get_tiles_from_call`

## Description

Returns the tiles corresponding to the call string. All tiles will
be found and returned in a list.

## Parameters

- `call_str`: `str`
    The call string.

## Returns

A list of `Tile`s.

> This function is very similar to `Action().get_tiles()`, but does not require an `Action` to be created. To use this function, you need to import the function from the `env.mahjong` module.

---

# Constructor

## Description
        
The constructor of the MahjongGame class.

## Parameters

- `ruleset`: `Ruleset`
    The ruleset of the game.
- `kwargs`:
    The keyword arguments. Accepts the following:
    - `wall`: `Wall` or `str` or `int`
        The wall to use. If a string is given, it will be interpreted as a file
        path. If an integer is given, it will be interpreted as the random seed.

# Method: `set_player`

## Description

Sets the player at the given index.

## Parameters

- `player_idx`: `int`
    The index of the player. (`0`, `1`, `2`, `3`)
- `player`: `Player`
    The player to set.

# Method: `initialize_game`

## Description

Initializes the game.

**This function resets the `state` attribute of the game, but will
not reset the `wall` attribute.** This means that the wall will NOT
be regenerated, but the game will be started over again.

The `state` attribute includes some crucial information that would be lost
when calling this function, such as `credits`.

# Method: `get_observation`

## Description

Gets the observation of the player.

## Parameters

- `player_idx`: `int`
    The index of the player to get the observation of.
- `additional_dict`: `dict` (optional)
    A dictionary of additional information to include in the observation.

## Returns

- `observation`: `dict`
    The observation of the player.

# Method: `get_state`

## Description

Gets the state of the game.

## Returns

A `dict` of the state of the game.

# Method: `play`

## Description

Plays the game.

# Additional Methods

There are quite a lot of additional methods in the `MahjongGame` class.
They are not documented mainly because the functions are not intended
to be used by the user, and the API may change regularly from version
to version.
