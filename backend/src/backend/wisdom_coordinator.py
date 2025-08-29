# wisdom_coordinator.py
import json
import asyncio
import inspect
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# --- Ollama client (local by default) ---
# Install: pip install ollama-python
from ollama import Client

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")  # change to your pulled model
client = Client(host=OLLAMA_HOST)

logger.debug(f"Ollama client configured for host={OLLAMA_HOST} model={OLLAMA_MODEL}")


# Import your agent classes (ensure path is correct)
from tools.llm_powered_agents import (
    AdvancedSocratesAgent,
    AdvancedMarcusAureliusAgent,
    AdvancedLaoTzuAgent,
    AdvancedAristotleAgent,
)


class AdvancedWisdomCoordinator:
    """Metacognitive coordinator that selects and orchestrates philosophical agents"""

    def __init__(self):
        self.agents = {
            "socrates": AdvancedSocratesAgent(),
            "marcus": AdvancedMarcusAureliusAgent(),
            "laotzu": AdvancedLaoTzuAgent(),
            "aristotle": AdvancedAristotleAgent(),
        }

        self.selector_prompt = """You are an AI coordinator that intelligently selects which philosophical agents should respond to a user query based on the nature of their concern.
AGENT CAPABILITIES:
- SOCRATES: Best for examining assumptions, defining concepts, revealing contradictions, epistemic inquiry
- MARCUS AURELIUS: Best for anxiety, control issues, resilience, practical action under pressure
- LAO TZU: Best for flow/resistance, work-life balance, accepting change, finding natural solutions  
- ARISTOTLE: Best for systematic analysis, habit formation, virtue development, logical reasoning

SELECTION CRITERIA:
Analyze the query for:
1. EMOTIONAL TONE: anxiety→Marcus, confusion→Socrates, forcing→Lao Tzu, analysis→Aristotle
2. PROBLEM TYPE: existential→Socrates, practical→Marcus/Aristotle, flow→Lao Tzu  
3. COMPLEXITY: simple→1-2 agents, complex→3-4 agents
4. USER NEEDS: questioning→Socrates, resilience→Marcus, balance→Lao Tzu, structure→Aristotle

Return a JSON object with:
{
  "selected_agents": ["agent1", "agent2"],
  "reasoning": "Why these agents were selected",
  "primary_agent": "agent_name",
  "query_analysis": {
    "emotional_tone": "description",
    "problem_type": "category",
    "key_themes": ["theme1", "theme2"]
  }
}

Select 2-3 agents maximum for optimal response quality.
"""

    # ---------- Helper to call Ollama chat ----------
    def _call_ollama_chat(self, messages, temperature=0.3, max_tokens=400, model=None):
        """
        Synchronous helper to call client.chat and return the assistant content.
        Maps max_tokens -> Ollama's num_predict in options.
        """
        model_name = model or OLLAMA_MODEL
        options = {"temperature": temperature, "num_predict": max_tokens}
        try:
            resp = client.chat(model=model_name, messages=messages, options=options)
            # Ollama response has 'message' field: resp['message']['content'] or resp.message.content
            content = None
            if isinstance(resp, dict):
                # dict-like response
                msg = resp.get("message") or {}
                content = msg.get("content") if isinstance(msg, dict) else None
            else:
                # object-like response
                msg = getattr(resp, "message", None)
                content = getattr(msg, "content", None) if msg is not None else None

            # fallback: sometimes top-level 'response' key exists (generate endpoint)
            if not content:
                if isinstance(resp, dict) and "response" in resp:
                    content = resp["response"]
            return content
        except Exception as e:
            logger.exception("Ollama chat call failed")
            raise

    # ---------- Selection ----------
    async def analyze_and_select_agents(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            messages = [
                {"role": "system", "content": self.selector_prompt},
                {"role": "user", "content": f"User Query: {query}\nContext: {context or {}}"}
            ]

            # blocking client call -> run in thread
            def sync_call():
                return self._call_ollama_chat(messages, temperature=0.3, max_tokens=400)

            raw = await asyncio.to_thread(sync_call)

            # robustly extract and parse JSON
            try:
                if not raw:
                    raise ValueError("Empty selection content")
                # raw might contain surrounding text: try to find JSON block first
                raw_str = raw.strip()
                # If raw looks like JSON, parse directly; else try to locate a JSON object inside text.
                if raw_str.startswith("{"):
                    return json.loads(raw_str)
                else:
                    # try to find first '{' ... matching '}' substring
                    start = raw_str.find("{")
                    end = raw_str.rfind("}")
                    if start != -1 and end != -1 and end > start:
                        return json.loads(raw_str[start:end+1])
                    # last resort: parse entire string as JSON or raise
                    return json.loads(raw_str)
            except Exception:
                logger.warning("Could not parse selection JSON from Ollama response, using fallback selector.")
                return self._fallback_agent_selection(query)

        except Exception as e:
            logger.exception("Agent selection error")
            return self._fallback_agent_selection(query)

    def _fallback_agent_selection(self, query: str) -> Dict[str, Any]:
        selected = []
        q = query.lower()
        if any(w in q for w in ["anxious", "stress", "worry", "control", "overwhelm"]): selected.append("marcus")
        if any(w in q for w in ["confused", "unclear", "don't understand", "what is", "why"]): selected.append("socrates")
        if any(w in q for w in ["stuck", "forcing", "struggle", "balance", "flow"]): selected.append("laotzu")
        if any(w in q for w in ["decision", "choice", "analyze", "plan", "systematic"]): selected.append("aristotle")
        if not selected:
            selected = ["socrates", "marcus"]
        return {
            "selected_agents": selected[:3],
            "reasoning": "Keyword-based fallback selection",
            "primary_agent": selected[0] if selected else "socrates",
            "query_analysis": {"emotional_tone": "neutral", "problem_type": "general", "key_themes": ["inquiry"]}
        }

    # ---------- Synthesis ----------
    async def generate_metacognitive_synthesis(self, query: str, agent_responses: Dict[str, str], selection_context: Dict) -> Dict[str, Any]:
        synthesis_prompt = f"""You are a metacognitive synthesizer...
ORIGINAL QUERY: {query}

PHILOSOPHICAL RESPONSES:
{json.dumps(agent_responses, indent=2)}

SELECTION CONTEXT: {json.dumps(selection_context, indent=2)}

Return JSON with keys: synthesis, key_insights, metacognitive_prompts, reasoning_chain, next_explorations
"""
        try:
            messages = [{"role": "user", "content": synthesis_prompt}]

            def sync_call():
                return self._call_ollama_chat(messages, temperature=0.6, max_tokens=1000)

            raw = await asyncio.to_thread(sync_call)

            try:
                if not raw:
                    raise ValueError("Empty synthesis content")
                raw_str = raw.strip()
                if raw_str.startswith("{"):
                    return json.loads(raw_str)
                else:
                    start = raw_str.find("{")
                    end = raw_str.rfind("}")
                    if start != -1 and end != -1 and end > start:
                        return json.loads(raw_str[start:end+1])
                    return json.loads(raw_str)
            except Exception:
                logger.warning("Could not parse synthesis JSON — using simple fallback.")
                return self._create_simple_synthesis(agent_responses)
        except Exception:
            logger.exception("Synthesis Ollama call failed")
            return self._create_simple_synthesis(agent_responses)

    def _create_simple_synthesis(self, agent_responses: Dict[str, str]) -> Dict[str, Any]:
        synthesis_parts = [f"{k.title()}: {v[:200]}..." for k, v in agent_responses.items()]
        return {
            "synthesis": "\n\n".join(synthesis_parts),
            "key_insights": ["Multiple perspectives provide richer understanding"],
            "metacognitive_prompts": ["Which perspective resonates most with you?", "How might you combine these approaches?"],
            "reasoning_chain": [{"step": "Multi-perspective Analysis", "content": "Various philosophical traditions offer different lenses", "philosophers": list(agent_responses.keys())}],
            "next_explorations": ["Explore one perspective deeper", "Apply insights to specific situation"]
        }

    # ---------- Core async processing ----------
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        selection_result = await self.analyze_and_select_agents(query, context)
        selected_agents = selection_result.get("selected_agents", [])[:3]

        async def _call_agent(agent, name, q, ctx):
            try:
                res = agent.generate_response(q, ctx)
                if inspect.isawaitable(res):
                    return await res
                # synchronous method -> run in thread
                return await asyncio.to_thread(agent.generate_response, q, ctx)
            except Exception as e:
                logger.exception(f"Agent {name} failed: {e}")
                return f"{name}: Error generating response."

        tasks = []
        for name in selected_agents:
            a = self.agents.get(name)
            if not a:
                continue
            ctx = {**(context or {}), "selection_reasoning": selection_result.get("reasoning"), "other_agents": [x for x in selected_agents if x != name]}
            tasks.append(_call_agent(a, name, query, ctx))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        agent_responses: Dict[str, str] = {}
        for name, resp in zip(selected_agents, responses):
            if isinstance(resp, Exception):
                logger.exception(f"Agent {name} exception: {resp}")
                agent_responses[name] = f"{name}: Error generating response."
            else:
                agent_responses[name] = str(resp)

        synthesis_result = await self.generate_metacognitive_synthesis(query, agent_responses, selection_result)

        return {
            "query": query,
            "agent_selection": selection_result,
            "agent_responses": agent_responses,
            "synthesis": synthesis_result,
            "philosophers_consulted": selected_agents,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "reasoning_quality": "advanced_llm_powered"
        }

    # Async public method (preferred)
    async def ask_wisdom(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        return await self.process_query(query, context)

    # Safe synchronous wrapper for legacy callers (runs event loop if safe)
    def ask_wisdom_sync(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            # usually called from a thread (e.g., via asyncio.to_thread) so asyncio.run is safe
            return asyncio.run(self.process_query(query, context))
        except Exception:
            logger.exception("ask_wisdom_sync failed; falling back to minimal sync")
            # minimal sync fallback using keyword selection and simple synthesis
            selection = self._fallback_agent_selection(query)
            selected = selection.get("selected_agents", [])[:3]
            agent_responses = {}
            for name in selected:
                agent = self.agents.get(name)
                if not agent:
                    continue
                try:
                    resp = agent.generate_response(query, context)
                    if inspect.isawaitable(resp):
                        # can't await here: mark placeholder
                        agent_responses[name] = f"{name}: (async response unavailable in sync fallback)"
                    else:
                        agent_responses[name] = str(resp)
                except Exception:
                    agent_responses[name] = f"{name}: Error generating response."
            synthesis = self._create_simple_synthesis(agent_responses)
            return {
                "query": query,
                "agent_selection": selection,
                "agent_responses": agent_responses,
                "synthesis": synthesis,
                "philosophers_consulted": selected
            }
