# main.py
import sys
import os
import inspect
import asyncio
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

p = FastAPI()
p.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # good for dev; in prod, specify e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add path for imports (keeps your original behavior)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the coordinator (ensure wisdom_coordinator.py / package exists)
from wisdom_coordinator import AdvancedWisdomCoordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WisdomArc - Advanced Philosophical AI",
    description="Revolutionary multi-agent philosophical reasoning system",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the advanced wisdom coordinator
# (If this constructor does heavy work, consider lazy init or moving into startup event)
wisdom_coordinator = AdvancedWisdomCoordinator()

class WisdomQuery(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None

# Keep response model flexible (you can replace with a strict Pydantic model later)
@app.get("/")
async def root():
    return {
        "message": "WisdomArc - Advanced Philosophical AI System",
        "version": "2.0.0",
        "description": "Multi-agent LLM-powered philosophical reasoning",
        "endpoints": {
            "POST /ask": "Get philosophical wisdom and reasoning",
            "GET /agents": "List available philosophical agents",
            "GET /health": "System health check"
        }
    }

@app.post("/ask", response_model=Dict[str, Any])
async def ask_wisdom(query: WisdomQuery):
    """
    Generate extraordinary philosophical responses using advanced LLM-powered agents.

    This handler safely supports coordinators whose `ask_wisdom` is either async or sync.
    """
    try:
        text = (query.text or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="Query text is empty.")

        logger.info(f"Processing wisdom query (first 120 chars): {text[:120]}")

        # Merge context and user_preferences into single context dictionary
        combined_context = {
            **(query.context or {}),
            **(query.user_preferences or {})
        } if (query.context or query.user_preferences) else None

        # Call coordinator in a safe way depending on its implementation
        ask_method = getattr(wisdom_coordinator, "ask_wisdom", None)
        if ask_method is None:
            raise RuntimeError("Coordinator does not expose `ask_wisdom` method.")

        # If ask_wisdom is an async function: await it
        if inspect.iscoroutinefunction(ask_method):
            result = await ask_method(text, combined_context)
        else:
            # If it's a sync function, run it in a thread so the event loop is not blocked
            result = await asyncio.to_thread(ask_method, text, combined_context)

        # Defensive: ensure result is a dict-like object
        if not isinstance(result, dict):
            logger.warning("Coordinator returned non-dict result; converting to dict.")
            # try to coerce simple structures into a dict
            result = {"result": str(result)}

        # Try to detect agent responses in common keys
        agent_responses = {}
        if isinstance(result.get("agent_responses"), dict):
            agent_responses = result["agent_responses"]
        elif isinstance(result.get("responses"), dict):
            agent_responses = result["responses"]
        else:
            # fallback: pick items that look like agent -> text
            candidate = {k: v for k, v in result.items() if isinstance(v, str)}
            # if candidate seems to contain many keys, assume it's agent responses
            if candidate and len(candidate) >= 1:
                agent_responses = candidate
            else:
                agent_responses = {}

        # philosophers consulted: try several common keys
        philosophers_consulted = result.get("philosophers_consulted") or result.get("philosophers") or list(agent_responses.keys())

        # agent selection and synthesis (if provided by coordinator)
        agent_selection = result.get("agent_selection", {})
        synthesis = result.get("synthesis")
        if not synthesis:
            # create a simple synthesis from agent_responses if missing
            synthesis = "\n\n".join(f"{name}: {resp}" for name, resp in agent_responses.items())

        # metadata merging
        metadata = result.get("metadata", {})
        metadata.update({
            "response_type": metadata.get("response_type", "advanced_llm_powered"),
            "system_version": metadata.get("system_version", "AAIRS 2.0"),
            "reasoning_depth": metadata.get("reasoning_depth", "metacognitive"),
            "agent_count": metadata.get("agent_count", len(philosophers_consulted) if philosophers_consulted else 0),
            "processing_status": "success",
            "timestamp_utc": datetime.utcnow().isoformat() + "Z"
        })

        enhanced_result = {
            "query": text,
            "agent_selection": agent_selection,
            "agent_responses": agent_responses,
            "synthesis": synthesis,
            "philosophers_consulted": philosophers_consulted,
            "metadata": metadata
        }

        # Ensure JSON-serializable before returning
        jsonable = jsonable_encoder(enhanced_result)
        logger.info(f"Wisdom generated successfully (agents: {len(jsonable.get('philosophers_consulted', []))})")
        return jsonable

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error processing wisdom query")
        raise HTTPException(status_code=500, detail=f"Wisdom processing error: {str(e)}")

@app.get("/agents")
async def list_agents():
    """List available philosophical agents and their capabilities"""
    return {
        "agents": {
            "socrates": {
                "name": "Socrates",
                "period": "470-399 BCE",
                "specialty": "Epistemic inquiry and assumption examination",
                "method": "Elenctic questioning and aporia induction",
                "best_for": ["Clarifying concepts", "Revealing assumptions", "Examining beliefs"]
            },
            "marcus": {
                "name": "Marcus Aurelius", 
                "period": "121-180 CE",
                "specialty": "Stoic resilience and practical wisdom",
                "method": "Dichotomy of control and virtue cultivation",
                "best_for": ["Anxiety management", "Building resilience", "Practical action"]
            },
            "laotzu": {
                "name": "Lao Tzu",
                "period": "6th century BCE",
                "specialty": "Natural harmony and effortless action",
                "method": "Wu wei and yin-yang balance",
                "best_for": ["Flow states", "Work-life balance", "Accepting change"]
            },
            "aristotle": {
                "name": "Aristotle",
                "period": "384-322 BCE", 
                "specialty": "Systematic analysis and virtue ethics",
                "method": "Golden mean and practical wisdom",
                "best_for": ["Habit formation", "Logical analysis", "Character development"]
            }
        },
        "capabilities": {
            "llm_powered": True,
            "contextual_selection": True,
            "metacognitive_synthesis": True,
            "reasoning_visualization": True
        }
    }

@app.get("/health")
async def health_check():
    """System health and status check"""
    try:
        test_agents = len(getattr(wisdom_coordinator, "agents", []))
        return {
            "status": "healthy",
            "agents_loaded": test_agents,
            "llm_integration": "active",
            "version": "2.0.0",
            "ready": True
        }
    except Exception as e:
        return {
            "status": "degraded", 
            "error": str(e),
            "ready": False
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
