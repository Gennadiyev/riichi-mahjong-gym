from flask import Flask, request, jsonify
import json
import os
import time

# Create a flask app
app = Flask("flask")

class MahjongServerState:
    IDLE = 0
    AWAIT = 1

server = {
    "observation": None,
    "action_space": None,
    "state": MahjongServerState.IDLE,
    "output_file": None
}

@app.route('/observation_update', methods=['POST'])
def observation_update():
    if server["state"] == MahjongServerState.IDLE:
        # Get incoming json
        req = request.get_json()
        # Update server info
        server["observation"] = json.loads(req["observation"])
        server["output_file"] = req["file"]
        server["state"] = MahjongServerState.AWAIT
        print(server["observation"])
        # Return json
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Server already has an observation"})

def legacy(action_space, obs):
    s = ""
    if len(action_space) == 1:
        print("Skipping player P{}\n".format(obs["player_idx"]))
        return action_space[0]
    s = "You: P{} / Current: P{}\n\n".format(obs["player_idx"], obs["active_player"])
    print("You: P{} / Current: P{}\n\n".format(obs["player_idx"], obs["active_player"]))
    s += "Observation: (STILL {} TILES)\n".format(obs["tiles_left"])
    if obs["incoming_tile"]:
        s += "Your Hand: " + obs["hand"].get_unicode_str() + " + " + obs["incoming_tile"].get_unicode_tile() + "\n"
    else:
        s += "Your Hand: " + obs["hand"].get_unicode_str() + "\n"
    
    s += "Dora Indicators: " + Deck(obs["dora_indicators"]).get_unicode_str() + "\n\n"
    s += "Action space: "
    for i in range(len(action_space)):
        s += "{:02d}: {} ".format(i, action_space[i].get_unicode_str())
    
    s += "\n\nDiscarded Tiles:\n"
    p = -1
    for discarded_tiles in obs["discarded_tiles"]:
        p += 1
        s += "> P{}: {}\n".format(p, Deck(discarded_tiles).get_unicode_str())

    s += "Calls:\n"
    p = -1
    for calls in obs["calls"]:
        p += 1
        s += "> P{}: ".format(p)
        for call in calls:
            action_string = call
            digits = [int(ch) for ch in action_string if ch.isdigit()]
            for digit_idx in range(0, len(digits), 2):
                id = digits[digit_idx] * 10 + digits[digit_idx+1]
                if id == 0:
                    break
                elif id == 60:
                    id = 0
                    break
                else:
                    tile = Tile(id)
                    action_string = action_string.replace(str(id), tile.get_unicode_tile())
            s += action_string + " / "
        if len(calls) > 0:
            s = s[:-3] + "\n"
        else:
            s += "-\n"
    s += "\n"
    return s

@app.route("/debug", methods=['GET'])
def debug():
    return "Debug\n\nState: {} \n\nObservation: {} \n\nAction Space: {}".format(server["state"], server["observation"], server["action_space"])

@app.route('/action_input', methods=['GET'])
def action_input():
    # Create human-readbale observation state
    if server["state"] == MahjongServerState.AWAIT:
        output = "<p>【<b>"
        wind = server["observation"]["wind"]
        if wind == "E":
            output += "東"
        elif wind == "S":
            output += "南"
        elif wind == "W":
            output += "西"
        elif wind == "N":
            output += "北"
        output += "</b>" + str(server["observation"]["wind_e"] + 1) + "局 · "
        output += str(server["observation"]["repeat"]) + "本場 · 供託" + "0" + "点 · 自風："
        output += ["東", "南", "西", "北", "東", "南", "西", "北"][server["observation"]["player_idx"] - server["observation"]["wind_e"] + 4]
        output += "】余" + str(server["observation"]["tiles_left"]) + '枚</p><p style="font-size:45px">'
        output += ''.join(server["observation"]["hand"]["tiles"]) + " + " + server["observation"]["incoming_tile"]["unicode"] + '</p><p style="font-size:30px">'
        output += '表ドラ表示: ' + ''.join([
            tile["unicode"] for tile in server["observation"]["dora_indicators"]
        ]) + "</p>"
        html = f"""<!DOCTYPE html><html>
<head>
    <title>Mahjong Action Input</title>
</head>
<body>
    <h1>Game State</h1>
    {output}
</body>
</html>
"""
        return html
    else:
        return "Waiting for observation"

# /action_submit?action=3, get parameter action
@app.route('/action_submit', methods=['GET'])
def action_submit():
    # Get action
    action = request.args.get('action')
    try:
        action = int(action)
    except:
        return jsonify({"success": False, "error": "Action is not an integer"})
    # Check if server is in AWAIT state
    if server["state"] == MahjongServerState.AWAIT:
        # Write action to file
        try:
            with open(server["output_file"], "w") as f:
                f.write(str(action))
        except:
            return jsonify({"success": False, "error": "Could not write to file " + server["output_file"]})
        # Update server state
        server["state"] = MahjongServerState.IDLE
        # Return json
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Server is not in AWAIT state"})


# Deploy at localhost:10317
app.run(host='localhost', port=10317, debug=True)

