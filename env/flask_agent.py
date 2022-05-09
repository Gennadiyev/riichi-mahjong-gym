from flask import Flask, request, jsonify
from env.agent import Agent

class FlaskAgent(Agent):
    '''
    Class: FlaskAgent
    '''

    def __init__(self, name):
        # Create a flask app
        self.app = Flask(name)
        # Create methods
        self.app.add_url_rule('/test', view_func=self.test)
        self.app.add_url_rule('/action', view_func=self.action)
        # Deploy at localhost:10317 without blocking the main thread
        import threading
        threading.Thread(target=self.app.run, kwargs={
            'host': 'localhost',
            'port': 10317,
            'debug': False
        }).start()

    def test(self):
        return jsonify({'test': 'test'})

    def query(self, obs, action_space):
        self.obs = obs
        self.action_space = action_space
    
    def action(self):
        return jsonify({'obs': self.obs, 'action_space': self.action_space})
