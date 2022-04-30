# Actions

Your agent, or model, interacts with the environment by selecting actions from the given action space.

An `Action` is a class that describes an action that can be performed.

## Action types and action strings

Here is the list of possible action types:

- `noop` (do nothing)
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

(no action string)

### `replace`

Cut (切る).

The action string should be the tile that is discarded.

E.g. `"41"` (cut 1z from hand)

### `reach`

Call reach (riichi, 立直).

The action string should be the tile that is discarded.
This action also calls reach.

E.g. `"r51"` (riichi with 0m), `"r60"` (richii with discard)

### `ron`

Call ron (ron, 和了).

*(no action string)*

### `tsumo`

Call tsumo (tsumo, 自摸).

*(no action string)*

### `ten`

Call ten (tenpai, 聴牌), i.e. the player has a waiting
hand by the end of a game.

*(no action string)*

### `noten`

Call noten (noten, ノーテン), i.e. the player does NOT
have a waiting hand by the end of a game.

*(no action string)*

## External links

The action strings defined here are inspired by the format used by [tenhou](https://tenhou.net/).
