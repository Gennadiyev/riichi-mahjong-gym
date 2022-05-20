from env.agent import Agent
import os
import time
import requests
import json

class FlaskAgent(Agent):
    '''
    Class: FlaskAgent
    '''

    def __init__(self, name, path: str, timeout: int = 60, server: str = "http://localhost:10317/"):
        super(FlaskAgent, self).__init__(name)
        self.path = path
        self.timeout = timeout
        self.server = server
        # Make sure the path exists
        # If path is relative path then make it absolute
        if not os.path.isabs(self.path):
            self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.path)
        # Make sure the path exists
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def query(self, obs, action_space):
        observation = obs
        action_space = action_space
        ret = requests.post(self.server + "observation_update", json={
            "observation": json.dumps(observation, default=lambda o: o.to_json()),
            "file": self.path,
            "action_space": json.dumps(action_space, default=lambda o: o.to_json()),
        })
        try:
            isSuccess = ret.json()["success"]
        except:
            isSuccess = False
        if not isSuccess:
            raise Exception("Error when posting observation to server")
        # Remove the file
        if os.path.exists(self.path):
            os.remove(self.path)
        # Wait for the file to be created
        t = time.time()
        while not os.path.exists(self.path):
            if time.time() - t > self.timeout:
                raise Exception("Timeout")
            time.sleep(0.9)
        # Read the file
        time.sleep(0.1)
        with open(self.path, "r") as f:
            action = f.read()
            try:
                action = int(action)
            except:
                raise Exception("Action is not an integer")
        raise Exception("Action receive: " + str(action))

