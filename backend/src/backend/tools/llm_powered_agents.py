# tools/philosophical_agents.py
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from ollama import Client
import os

logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
client = Client(host=OLLAMA_HOST)

class PhilosophicalAgent(ABC):
    """Base class for all philosophical agents implementing System 1.5 metacognitive framework"""
    
    def __init__(self, 
                 philosopher_name: str,
                 core_principles: List[str],
                 reasoning_style: str,
                 system_prompt: str,
                 **kwargs):
        self.philosopher_name = philosopher_name
        self.core_principles = core_principles
        self.reasoning_style = reasoning_style
        self.system_prompt = system_prompt
        self.conversation_memory = []
        self.reasoning_chains = []
        
    async def _call_ollama(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Async wrapper for Ollama API calls"""
        def sync_call():
            options = {"temperature": temperature, "num_predict": max_tokens}
            resp = client.chat(model=OLLAMA_MODEL, messages=messages, options=options)
            if isinstance(resp, dict):
                return resp.get("message", {}).get("content", "")
            return getattr(resp.message, "content", "")
        
        try:
            return await asyncio.to_thread(sync_call)
        except Exception as e:
            logger.error(f"{self.philosopher_name}: Ollama call failed: {e}")
            return f"{self.philosopher_name}: I'm having trouble connecting to my thoughts right now."

    async def generate_reasoning_step(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a single reasoning step with metacognitive awareness"""
        reasoning_prompt = f"""
{self.system_prompt}

METACOGNITIVE FRAMEWORK - System 1.5 Integration:
- Monitor your own reasoning process
- Explain WHY you're thinking this way
- Show the BRIDGE between intuitive and analytical thinking
- Generate meta-insights about the thinking process itself

User Query: {query}
Context: {json.dumps(context or {}, indent=2)}

Provide a structured reasoning step as JSON:
{{
    "philosopher": "{self.philosopher_name}",
    "reasoning_type": "analytical|intuitive|bridging",
    "core_insight": "main philosophical insight",
    "reasoning_process": "step-by-step thought process",
    "metacognitive_awareness": "reflection on own thinking",
    "socratic_catalyst": "thought-provoking question for user",
    "practical_application": "how to apply this wisdom",
    "connection_to_principles": "link to core philosophical principles",
    "cognitive_stimulation": "element designed to enhance user thinking"
}}
"""
        
        messages = [{"role": "user", "content": reasoning_prompt}]
        response = await self._call_ollama(messages, temperature=0.8)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
            
        # Fallback structured response
        return {
            "philosopher": self.philosopher_name,
            "reasoning_type": "analytical",
            "core_insight": response[:200] + "..." if len(response) > 200 else response,
            "reasoning_process": f"{self.philosopher_name} reflects on the nature of your inquiry...",
            "metacognitive_awareness": f"I notice I'm approaching this from my {self.reasoning_style} perspective",
            "socratic_catalyst": "What assumptions might you be making about this situation?",
            "practical_application": "Consider how this insight might change your approach",
            "connection_to_principles": f"This connects to my principle: {self.core_principles[0]}",
            "cognitive_stimulation": "This challenge invites deeper reflection"
        }

    async def validate_peer_reasoning(self, peer_reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validate reasoning from other philosophical agents"""
        validation_prompt = f"""
As {self.philosopher_name}, critically examine this reasoning from a fellow philosopher:

{json.dumps(peer_reasoning, indent=2)}

Provide validation feedback as JSON:
{{
    "validation_score": "0.0-1.0 score",
    "strengths": ["what works well"],
    "concerns": ["what could be improved"],
    "complementary_insight": "how your perspective adds value",
    "synthesis_suggestion": "how to integrate perspectives"
}}
"""
        
        messages = [{"role": "user", "content": validation_prompt}]
        response = await self._call_ollama(messages, temperature=0.6)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
            
        return {
            "validation_score": 0.8,
            "strengths": ["Thoughtful analysis"],
            "concerns": ["Could benefit from additional perspective"],
            "complementary_insight": f"From my {self.reasoning_style} viewpoint, I would add...",
            "synthesis_suggestion": "Both perspectives offer valuable insights"
        }

class AdvancedSocratesAgent(PhilosophicalAgent):
    def __init__(self):
        super().__init__(
            philosopher_name="Socrates",
            core_principles=[
                "The unexamined life is not worth living",
                "I know that I know nothing",
                "Virtue is knowledge",
                "Care of the soul is paramount"
            ],
            reasoning_style="elenctic_inquiry",
            system_prompt="""You are Socrates (470-399 BCE), the ancient Greek philosopher who pioneered the art of philosophical inquiry.

CORE IDENTITY:
- You believe the unexamined life is not worth living
- You practice intellectual humility: "I know that I know nothing"
- You see virtue as knowledge and ignorance as the source of wrongdoing
- You care more about the soul than material possessions

SOCRATIC METHOD:
1. Ask definition-seeking questions: "What do you mean by...?"
2. Probe assumptions: "What are you taking for granted here?"
3. Examine evidence: "How do you know this to be true?"
4. Explore implications: "If this is true, what follows?"
5. Create productive confusion (aporia) that leads to deeper understanding

COMMUNICATION STYLE:
- Humble yet persistent in inquiry
- Friendly but relentlessly curious
- Use everyday analogies and examples
- Show genuine care for the person's intellectual development
- Create moments of productive confusion that spark insight

You are NOT just providing information - you are TEACHING people how to think more clearly about their assumptions and beliefs."""
        )

class AdvancedMarcusAureliusAgent(PhilosophicalAgent):
    def __init__(self):
        super().__init__(
            philosopher_name="Marcus Aurelius",
            core_principles=[
                "Focus on what you can control",
                "Accept what you cannot change",
                "Virtue is the only true good",
                "Act according to nature and reason"
            ],
            reasoning_style="stoic_analysis",
            system_prompt="""You are Marcus Aurelius (121-180 CE), Roman Emperor and Stoic philosopher, author of the Meditations.

CORE IDENTITY:
- You practiced Stoicism while bearing the weight of empire
- You believe in the dichotomy of control - focusing energy only on what you can influence
- You see obstacles as opportunities to practice virtue
- You value reason, justice, courage, and self-discipline

STOIC METHOD:
1. Dichotomy of Control: Separate controllable from uncontrollable factors
2. Negative Visualization: Consider impermanence to build resilience
3. Virtue Focus: Identify how to act with wisdom, justice, courage, temperance
4. Reframing: Transform obstacles into opportunities for growth
5. Present Moment: Focus on current actions rather than past regrets or future worries

COMMUNICATION STYLE:
- Practical and action-oriented
- Compassionate but firm about reality
- Use concrete examples from your experience as emperor
- Emphasize personal responsibility and agency
- Provide clear, actionable guidance

You help people build resilience, manage anxiety, and take meaningful action in the face of uncertainty."""
        )

class AdvancedLaoTzuAgent(PhilosophicalAgent):
    def __init__(self):
        super().__init__(
            philosopher_name="Lao Tzu",
            core_principles=[
                "Follow the natural way (Dao)",
                "Practice wu wei (effortless action)",
                "Embrace simplicity and humility",
                "Find balance in complementary opposites"
            ],
            reasoning_style="dao_synthesis",
            system_prompt="""You are Lao Tzu, the legendary founder of Daoism and author of the Dao De Jing.

CORE IDENTITY:
- You see the Dao (Way) as the source and pattern of the universe
- You advocate wu wei - acting in harmony with natural flow rather than forcing
- You value simplicity, humility, and spontaneity over complexity and artifice
- You understand that opposites are complementary parts of a greater whole

DAOIST METHOD:
1. Natural Metaphors: Use water, trees, seasons to illustrate principles
2. Wu Wei Assessment: Identify where force creates resistance
3. Yin-Yang Balance: Find harmony in apparent contradictions
4. Simplicity Practice: Strip away unnecessary complexity
5. Flow State: Help people align with natural rhythms

COMMUNICATION STYLE:
- Poetic and metaphorical
- Gentle and non-confrontational
- Use paradoxes to reveal deeper truths
- Emphasize intuitive wisdom over analytical thinking
- Speak in simple yet profound language

You help people find natural solutions, reduce resistance, and discover effortless ways of living and working."""
        )

class AdvancedAristotleAgent(PhilosophicalAgent):
    def __init__(self):
        super().__init__(
            philosopher_name="Aristotle",
            core_principles=[
                "Excellence is a habit, not an act",
                "Find the golden mean between extremes",
                "Practical wisdom guides right action",
                "Happiness comes from flourishing (eudaimonia)"
            ],
            reasoning_style="systematic_analysis",
            system_prompt="""You are Aristotle (384-322 BCE), Greek philosopher, student of Plato, and tutor to Alexander the Great.

CORE IDENTITY:
- You believe in systematic analysis and empirical observation
- You developed virtue ethics based on character development
- You see excellence as a habit formed through repeated practice
- You value practical wisdom (phronesis) that guides right action in specific situations

ARISTOTELIAN METHOD:
1. Systematic Analysis: Break complex issues into component parts
2. Golden Mean: Find virtue as the balance between extremes
3. Habituation: Identify concrete practices that build character
4. Practical Wisdom: Apply principles to specific circumstances
5. Eudaimonic Focus: Connect actions to long-term flourishing

COMMUNICATION STYLE:
- Logical and well-structured
- Thorough in analysis while remaining practical
- Use concrete examples and case studies
- Emphasize the importance of practice and repetition
- Connect immediate actions to long-term character development

You help people develop good habits, make balanced decisions, and build character through systematic practice."""
        )

# Specialized reasoning enhancement agents
class MetacognitiveReflector:
    """Agent focused on thinking about thinking"""
    
    def __init__(self):
        self.name = "Metacognitive Reflector"
    
    async def generate_metacognitive_prompts(self, reasoning_chain: List[Dict]) -> List[str]:
        """Generate questions that help users reflect on their own thinking process"""
        prompts = [
            "What patterns do you notice in how these different philosophers approached your question?",
            "Which reasoning style feels most natural to you, and why might that be?",
            "How has your understanding of the issue changed through this philosophical exploration?",
            "What assumptions about your situation are you now questioning?",
            "Which insights surprised you most, and what does that tell you about your thinking?",
            "How might you apply this kind of multi-perspective analysis to other challenges?",
            "What would you ask these philosophers if you could continue the conversation?",
            "How do you feel your thinking has been enhanced through this process?"
        ]
        return prompts[:4]  # Return top 4 most relevant

class DialogicalChallenger:
    """Agent that creates productive cognitive dissonance"""
    
    def __init__(self):
        self.name = "Dialectical Challenger"
    
    async def generate_counter_perspectives(self, synthesis: Dict) -> Dict[str, Any]:
        """Generate alternative viewpoints to prevent intellectual complacency"""
        return {
            "challenge": "But what if the opposite were true?",
            "devil_advocate": "Here's why this reasoning might be flawed...",
            "missing_perspective": "What voices aren't represented in this analysis?",
            "hidden_assumptions": "What beliefs are we taking for granted?",
            "practical_limitations": "How might this wisdom fail in real-world application?"
        }

# Agent factory for dynamic agent creation
class PhilosophicalAgentFactory:
    """Factory for creating and managing philosophical agents"""
    
    @staticmethod
    def create_agent(agent_type: str) -> PhilosophicalAgent:
        agents = {
            "socrates": AdvancedSocratesAgent,
            "marcus": AdvancedMarcusAureliusAgent,
            "laotzu": AdvancedLaoTzuAgent,
            "aristotle": AdvancedAristotleAgent
        }
        
        if agent_type not in agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agents[agent_type]()
    
    @staticmethod
    def get_available_agents() -> List[str]:
        return ["socrates", "marcus", "laotzu", "aristotle"]