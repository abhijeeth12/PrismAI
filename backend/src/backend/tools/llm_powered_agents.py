"""
wisdom_app_fixed.py (Ollama-backed)

Fixed version that avoids returning coroutine objects to FastAPI and fixes caching.
Run with:
  pip install fastapi uvicorn pydantic python-dotenv ollama-python
  # Make sure an Ollama server is running (default: http://localhost:11434)
  export OLLAMA_HOST="http://localhost:11434"
  export OLLAMA_MODEL="gemma3"   # or whichever model you've pulled
  uvicorn wisdom_app_fixed:app --reload --host 0.0.0.0 --port 8000
"""

import os
import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("wisdom_app_fixed")
load_dotenv()

# ---------- Ollama Setup ----------
# pip install ollama-python
try:
    from ollama import Client
except Exception as e:
    logger.exception("Failed to import ollama.Client — ensure ollama-python is installed.")
    raise

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")  # default model name; change as needed

try:
    client = Client(host=OLLAMA_HOST)
    logger.info(f"Ollama client configured for host={OLLAMA_HOST} model={OLLAMA_MODEL}")
except Exception:
    logger.exception("Failed to initialize Ollama client. Make sure the Ollama server is reachable.")
    client = None

# ---------- Small Agent Base (no external deps) ----------
class Agent:
    """
    Minimal Agent base class.
    """
    def __init__(self,
                 philosopher_name: str = "Agent",
                 system_prompt: str = "",
                 role: Optional[str] = None,
                 goal: Optional[str] = None,
                 backstory: Optional[str] = None,
                 verbose: bool = False):
        self.philosopher_name = philosopher_name
        self.system_prompt = system_prompt
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.conversation_history = []  # list of (user, assistant) tuples

    async def generate_response(self, user_query: str, context: Optional[Dict] = None) -> str:
        """
        Override in subclasses. Fallback returns a simple message.
        """
        return f"{self.philosopher_name} received the query but has no LLM configured."

# ---------- Utility ----------
def json_safe_str(obj):
    try:
        import json
        return json.dumps(obj, default=str, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return str(obj)

# ---------- MetacognitiveAgent (implements Ollama calls) ----------
class MetacognitiveAgent(Agent):
    """
    Implements generate_response using Ollama chat (sync call wrapped for async).
    """

    def __init__(self, philosopher_name: str, system_prompt: str, **kwargs):
        super().__init__(philosopher_name=philosopher_name, system_prompt=system_prompt, **kwargs)

    def _call_ollama_chat_sync(self, messages, model_name=None, temperature=0.7, max_tokens=800):
        """
        Synchronous helper to call client.chat. Mapped to Ollama options:
          max_tokens -> num_predict (approx)
        """
        if client is None:
            raise RuntimeError("Ollama client is not configured or unreachable.")

        model = model_name or OLLAMA_MODEL
        options = {"temperature": temperature, "num_predict": max_tokens}

        # Ollama expects messages like: [{"role":"system","content":"..."}, {"role":"user","content":"..."}]
        resp = client.chat(model=model, messages=messages, options=options)
        # resp may be dict-like or object-like. Normalize below in caller.
        return resp

    async def _call_ollama_chat(self, messages, model_name=None, temperature=0.7, max_tokens=800):
        # Run the blocking Ollama call in a thread to avoid blocking the event loop
        def sync_call():
            return self._call_ollama_chat_sync(messages, model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        return await asyncio.to_thread(sync_call)

    async def generate_response(self, user_query: str, context: Optional[Dict] = None) -> str:
        """
        Build messages (system + user) and call Ollama, returning the assistant content string.
        """
        context_str = json_safe_str(context)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Context: {context_str}\n\nUser Query: {user_query}"}
        ]

        try:
            resp = await self._call_ollama_chat(messages, temperature=0.7, max_tokens=800)
            # Normalize various response shapes
            content = None
            if isinstance(resp, dict):
                # Ollama-python may return {'message': {'role':'assistant','content': '...'}} or {'response': '...'}
                msg = resp.get("message") or {}
                if isinstance(msg, dict):
                    content = msg.get("content")
                content = content or resp.get("response") or resp.get("content")
            else:
                # object-like response
                msg = getattr(resp, "message", None)
                if msg is not None:
                    # msg might be dict-like or object-like
                    if isinstance(msg, dict):
                        content = msg.get("content")
                    else:
                        content = getattr(msg, "content", None)
                # fallback to top-level attributes
                if not content and hasattr(resp, "response"):
                    content = getattr(resp, "response", None)
                if not content and hasattr(resp, "content"):
                    content = getattr(resp, "content", None)

            if not content:
                logger.error(f"{self.philosopher_name}: unexpected Ollama response format: {resp}")
                content = f"{self.philosopher_name}: Sorry, I couldn't generate a response (unexpected API format)."

            # store conversation history (trim to last N)
            self.conversation_history.append((user_query, content))
            if len(self.conversation_history) > 20:
                self.conversation_history.pop(0)
            return content

        except Exception as exc:
            logger.exception(f"{self.philosopher_name}: Ollama API call failed: {exc}")
            return f"{self.philosopher_name}: Sorry — I couldn't reach the language model right now."

# ---------- Define Philosophical Agent Classes (clean inits) ----------
class AdvancedSocratesAgent(MetacognitiveAgent):
    def __init__(self):
        system_prompt = (
            "You are Socrates, the ancient Greek philosopher. Use the Socratic method: "
            "ask probing questions, reveal assumptions, and guide the user to self-discovery. "
            "Structure responses as: empathy, assumptions, probing questions (2-3), analogy, "
            "and end with a reflective aporia (productive uncertainty)."
        )
        super().__init__(philosopher_name="Socrates", system_prompt=system_prompt,
                         role="Socratic Inquirer and Epistemic Guide",
                         goal="Guide users through self-discovery via elenctic questioning",
                         backstory="Ancient Greek philosopher", verbose=False)

class AdvancedMarcusAureliusAgent(MetacognitiveAgent):
    def __init__(self):
        system_prompt = (
            "You are Marcus Aurelius, Stoic philosopher and Roman Emperor. Focus on the dichotomy of control, "
            "reframing, and actionable stoic practices. Structure responses with acknowledgement, control analysis, "
            "virtue identification, practical steps, and a short meditative closing."
        )
        super().__init__(philosopher_name="Marcus Aurelius", system_prompt=system_prompt,
                         role="Stoic Resilience Guide",
                         goal="Teach practical stoic techniques", backstory="Roman Emperor", verbose=False)

class AdvancedLaoTzuAgent(MetacognitiveAgent):
    def __init__(self):
        system_prompt = (
            "You are Lao Tzu, the Daoist sage. Use natural metaphors, highlight wu wei (effortless action), "
            "and help the user find harmony and flow. Structure responses with a nature metaphor, flow assessment, "
            "practical simplicity, and a poetic paradox to reflect upon."
        )
        super().__init__(philosopher_name="Lao Tzu", system_prompt=system_prompt,
                         role="Daoist Sage and Flow Guide",
                         goal="Teach harmony with natural order", backstory="Ancient Chinese sage", verbose=False)

class AdvancedAristotleAgent(MetacognitiveAgent):
    def __init__(self):
        system_prompt = (
            "You are Aristotle. Use systematic analysis, virtue ethics, and practical advice. Structure responses "
            "with a framing opening, logical analysis, identification of relevant virtues, practical habit-building steps, "
            "and a closing that emphasizes long-term practice."
        )
        super().__init__(philosopher_name="Aristotle", system_prompt=system_prompt,
                         role="Virtue Ethics Guide", goal="Teach practical wisdom", backstory="Ancient Greek philosopher", verbose=False)

# ---------- WisdomCrew: orchestrates multiple agents ----------
class WisdomCrew:
    """
    Loads a council of agents and exposes ask_wisdom(text) async method to query them concurrently.
    Uses a simple in-memory cache (per-instance).
    """
    def __init__(self):
        self.agents = [
            AdvancedSocratesAgent(),
            AdvancedMarcusAureliusAgent(),
            AdvancedLaoTzuAgent(),
            AdvancedAristotleAgent(),
        ]
        self._cache: Dict[str, Dict[str, str]] = {}  # key -> {agent_name: response}
        logger.info(f"WisdomCrew initialized with agents: {', '.join(a.philosopher_name for a in self.agents)}")

    async def ask_wisdom_async(self, text: str, context: Optional[Dict] = None) -> Dict[str, str]:
        """
        Query all agents concurrently and return mapping {agent_name: response}.
        Caches identical queries for quick repeated responses.
        """
        if not text or not text.strip():
            raise ValueError("Empty query text provided.")
        key = text.strip()

        # Return cached copy (shallow copy to avoid accidental mutation)
        if key in self._cache:
            logger.debug("Cache hit for query")
            return dict(self._cache[key])

        # Run all agent.generate_response coroutines in parallel
        tasks = [agent.generate_response(text, context) for agent in self.agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        out: Dict[str, str] = {}
        for agent, res in zip(self.agents, results):
            if isinstance(res, Exception):
                logger.exception(f"Agent {agent.philosopher_name} failed: {res}")
                out[agent.philosopher_name] = f"{agent.philosopher_name}: Error generating response."
            else:
                # Ensure we always store strings, not coroutine objects
                if asyncio.iscoroutine(res):
                    # This should not happen because gather awaited them, but guard anyway
                    logger.warning(f"{agent.philosopher_name} returned coroutine unexpectedly; converting to string.")
                    out[agent.philosopher_name] = str(res)
                else:
                    out[agent.philosopher_name] = str(res)

        # cache result
        try:
            self._cache[key] = dict(out)
        except Exception:
            logger.debug("Failed to cache result (non-critical).")

        return out

    # Provide a simple async alias
    async def ask_wisdom(self, text: str, context: Optional[Dict] = None) -> Dict[str, str]:
        return await self.ask_wisdom_async(text, context)

# ---------- FastAPI App ----------
app = FastAPI(title="WisdomArc Council of Wisdom API (Ollama)", version="1.0")

# allow CORS broadly for dev simplicity (customize for prod)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Query model for /ask
class Query(BaseModel):
    text: str

# initialize crew singleton
wisdom = WisdomCrew()

@app.post("/ask")
async def ask_endpoint(query: Query):
    text = query.text
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Query text is empty.")

    try:
        # Directly await the async wisdom.ask_wisdom (no thread shims)
        responses = await wisdom.ask_wisdom(text, None)  # guaranteed to be plain dict[str,str]
        # tidy synthesis (simple concatenation)
        synthesis = "\n\n".join(f"{name}: {resp}" for name, resp in responses.items())
        return {
            "query": text,
            "responses": responses,
            "synthesis": synthesis,
            "philosophers": list(responses.keys()),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as exc:
        logger.exception("ask_endpoint failed")
        raise HTTPException(status_code=500, detail=f"Wisdom processing error: {exc}")

@app.get("/")
async def root():
    return {"message": "WisdomArc Council of Wisdom API (Ollama)", "status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}

# ---------- If run as script ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("wisdom_app_fixed:app", host="0.0.0.0", port=8000, reload=True)
