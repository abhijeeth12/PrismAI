import yaml
from crewai import Crew, Process
from tools.advanced_agents import (
    AdvancedSocratesAgent,
    AdvancedMarcusAureliusAgent, 
    AdvancedLaoTzuAgent,
    AdvancedAristotleAgent
)


class WisdomCrew:
    def __init__(self):
        # Initialize agents directly without YAML complexity
        self.agents = {
            "socrates": AdvancedSocratesAgent(),
            "marcus": AdvancedMarcusAureliusAgent(),
            "laotzu": AdvancedLaoTzuAgent(),
            "aristotle": AdvancedAristotleAgent()
        }
    
    def ask_wisdom(self, query):
        if isinstance(query, dict):
            text = query.get("text", "")
        else:
            text = str(query)
        responses = {}
        for name, agent in self.agents.items():
            responses[name] = agent.generate_response(text)
        return responses


