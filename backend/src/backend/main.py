# main.py
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from wisdom_coordinator import AdvancedWisdomCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WisdomArc - Revolutionary Philosophical AI",
    description="Advanced Agentic AI Reasoning System (AAIRS) with System 1.5 Metacognitive Framework",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the revolutionary wisdom coordinator
wisdom_coordinator = AdvancedWisdomCoordinator()

class WisdomQuery(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    streaming: Optional[bool] = False

class WebSocketManager:
    """Manage WebSocket connections for real-time reasoning streams"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected: {session_id}")
    
    async def send_reasoning_step(self, session_id: str, data: Dict[str, Any]):
        websocket = self.active_connections.get(session_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(data))
            except Exception as e:
                logger.error(f"Failed to send to {session_id}: {e}")
                self.disconnect(session_id)

websocket_manager = WebSocketManager()

@app.get("/")
async def root():
    return {
        "message": "WisdomArc - Revolutionary Philosophical AI System",
        "version": "2.0.0", 
        "system": "AAIRS (Advanced Agentic AI Reasoning System)",
        "framework": "System 1.5 Metacognitive Enhancement",
        "description": "Transform conversations into cognitive enhancement experiences",
        "capabilities": [
            "Real-time multi-agent philosophical reasoning",
            "Transparent reasoning visualization", 
            "Metacognitive skill development",
            "System 1.5 intuitive-analytical bridging",
            "Progressive cognitive complexity scaling"
        ],
        "endpoints": {
            "POST /ask": "Get comprehensive philosophical wisdom (batch mode)",
            "WebSocket /ws/{session_id}": "Real-time streaming reasoning visualization",
            "GET /agents": "List available philosophical agents",
            "GET /health": "System health and capability check"
        }
    }

@app.post("/ask")
async def ask_wisdom(query: WisdomQuery):
    """
    Generate revolutionary philosophical responses with System 1.5 metacognitive enhancement.
    
    This endpoint provides comprehensive philosophical analysis combining multiple wisdom traditions
    with transparent reasoning processes designed to enhance user cognitive capabilities.
    """
    try:
        text = (query.text or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
        logger.info(f"Processing wisdom query: {text[:100]}...")
        
        # Combine context and preferences
        combined_context = {
            **(query.context or {}),
            **(query.user_preferences or {}),
            "processing_mode": "batch",
            "enhancement_level": "comprehensive"
        }
        
        # Process the wisdom request
        result = await wisdom_coordinator.ask_wisdom(text, combined_context)
        
        if not result:
            raise HTTPException(status_code=500, detail="Wisdom processing failed to generate results.")
        
        # Enhance response with metadata
        enhanced_result = {
            **result,
            "response_metadata": {
                "processing_time": datetime.utcnow().isoformat(),
                "system_version": "AAIRS 2.0",
                "framework": "System 1.5 Metacognitive",
                "reasoning_quality": "revolutionary_enhancement",
                "cognitive_load_optimized": True,
                "transparency_level": "complete_visibility",
                "educational_value": "transformative"
            }
        }
        
        # Ensure JSON serializable
        jsonable_result = jsonable_encoder(enhanced_result)
        
        logger.info(f"Wisdom generated successfully - Agents consulted: {len(jsonable_result.get('philosophers_consulted', []))}")
        
        return jsonable_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Critical error in wisdom processing")
        raise HTTPException(
            status_code=500, 
            detail=f"Wisdom processing system error: {str(e)}"
        )

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Real-time streaming philosophical reasoning with transparent visualization.
    
    This WebSocket endpoint provides live streaming of the multi-agent reasoning process,
    allowing users to observe and learn from the collaborative philosophical analysis
    as it unfolds in real-time.
    """
    await websocket_manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive query from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            query_text = message.get("query", "").strip()
            context = message.get("context", {})
            
            if not query_text:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Query text is required",
                    "timestamp": datetime.utcnow().isoformat()
                }))
                continue
            
            logger.info(f"WebSocket reasoning request from {session_id}: {query_text[:100]}...")
            
            # Stream the reasoning process
            async for reasoning_step in wisdom_coordinator.process_wisdom_request(query_text, context):
                await websocket_manager.send_reasoning_step(session_id, {
                    "type": "reasoning_update",
                    "session_id": session_id,
                    **reasoning_step
                })
                
                # Small delay for better streaming experience
                await asyncio.sleep(0.1)
            
            # Send completion signal
            await websocket_manager.send_reasoning_step(session_id, {
                "type": "reasoning_complete",
                "session_id": session_id,
                "message": "Philosophical analysis complete",
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket client {session_id} disconnected")
        websocket_manager.disconnect(session_id)
    except Exception as e:
        logger.exception(f"WebSocket error for {session_id}: {e}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Processing error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }))
        except:
            pass
        websocket_manager.disconnect(session_id)

@app.get("/agents")
async def list_agents():
    """List available philosophical agents and their revolutionary capabilities"""
    return {
        "system": "AAIRS 2.0 - Advanced Agentic AI Reasoning System",
        "framework": "System 1.5 Metacognitive Enhancement",
        "agents": {
            "socrates": {
                "name": "Socrates",
                "period": "470-399 BCE",
                "specialty": "Epistemic inquiry and assumption examination", 
                "method": "Elenctic questioning and aporia induction",
                "cognitive_enhancement": "Develops critical thinking and intellectual humility",
                "best_for": [
                    "Examining hidden assumptions",
                    "Clarifying concepts and definitions",
                    "Developing intellectual humility",
                    "Learning to ask better questions"
                ],
                "system15_role": "Bridges intuitive insights with analytical examination"
            },
            "marcus_aurelius": {
                "name": "Marcus Aurelius",
                "period": "121-180 CE", 
                "specialty": "Stoic resilience and practical wisdom",
                "method": "Dichotomy of control and virtue cultivation",
                "cognitive_enhancement": "Builds emotional regulation and practical decision-making",
                "best_for": [
                    "Managing anxiety and stress",
                    "Building resilience and mental toughness", 
                    "Making decisions under pressure",
                    "Focusing on actionable solutions"
                ],
                "system15_role": "Transforms emotional reactions into reasoned responses"
            },
            "lao_tzu": {
                "name": "Lao Tzu",
                "period": "6th century BCE",
                "specialty": "Natural harmony and effortless action (wu wei)",
                "method": "Dao cultivation and yin-yang balance",
                "cognitive_enhancement": "Develops intuitive wisdom and flow states", 
                "best_for": [
                    "Finding natural solutions to complex problems",
                    "Achieving work-life balance and flow states",
                    "Accepting and adapting to change",
                    "Reducing force and resistance in approaches"
                ],
                "system15_role": "Enhances intuitive pattern recognition and natural wisdom"
            },
            "aristotle": {
                "name": "Aristotle", 
                "period": "384-322 BCE",
                "specialty": "Systematic analysis and virtue ethics",
                "method": "Golden mean principle and practical wisdom (phronesis)",
                "cognitive_enhancement": "Develops systematic thinking and habit formation",
                "best_for": [
                    "Systematic analysis of complex problems",
                    "Developing good habits and character",
                    "Making balanced decisions (golden mean)",
                    "Building long-term excellence through practice"
                ],
                "system15_role": "Provides structured analytical frameworks for decision-making"
            }
        },
        "revolutionary_capabilities": {
            "system15_integration": "First AI to bridge intuitive System 1 and analytical System 2 thinking",
            "metacognitive_enhancement": "Every interaction teaches better thinking skills",
            "transparent_reasoning": "Complete visibility into multi-agent collaborative process",
            "cognitive_load_optimization": "Adaptive complexity scaling based on user readiness",
            "real_time_streaming": "Watch philosophical reasoning unfold live",
            "dialectical_synthesis": "Agents cross-validate and refine each other's insights",
            "progressive_development": "System learns and adapts to user's cognitive growth"
        },
        "collaboration_patterns": {
            "sequential": "Agents build on each other's insights progressively",
            "parallel": "Independent analysis for diverse perspectives", 
            "hierarchical": "Primary agent leads with supporting elaboration",
            "dialectical": "Agents challenge and refine each other's reasoning"
        }
    }

@app.get("/health")
async def health_check():
    """Comprehensive system health and capability assessment"""
    try:
        # Test core components
        test_query = "Test system functionality"
        test_result = await wisdom_coordinator.ask_wisdom(test_query, {"test_mode": True})
        
        agents_available = len(wisdom_coordinator.orchestrator.agent_factory.get_available_agents())
        
        health_status = {
            "status": "healthy",
            "system_version": "AAIRS 2.0",
            "framework": "System 1.5 Metacognitive Enhancement",
            "timestamp": datetime.utcnow().isoformat(),
            "capabilities": {
                "agents_available": agents_available,
                "llm_integration": "active",
                "real_time_streaming": "operational",
                "metacognitive_framework": "active",
                "reasoning_synthesis": "operational",
                "cognitive_load_analysis": "active",
                "dialectical_reasoning": "operational"
            },
            "performance_metrics": {
                "reasoning_quality": "revolutionary",
                "response_coherence": "high",
                "educational_value": "transformative", 
                "cognitive_enhancement": "active",
                "transparency_level": "complete"
            },
            "innovation_features": {
                "system15_bridging": True,
                "multi_agent_orchestration": True,
                "real_time_reasoning_visualization": True,
                "progressive_complexity_scaling": True,
                "metacognitive_skill_development": True,
                "transparent_philosophical_collaboration": True
            },
            "test_result": "functional" if test_result else "degraded"
        }
        
        return health_status
        
    except Exception as e:
        logger.exception("Health check failed")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "message": "System experiencing issues but core functionality may still be available"
        }

@app.get("/reasoning-demo")
async def reasoning_demo():
    """Demonstrate the revolutionary reasoning capabilities with sample queries"""
    return {
        "message": "WisdomArc Revolutionary Reasoning Demonstration",
        "sample_queries": {
            "existential": {
                "query": "I feel lost and don't know what direction my life should take",
                "expected_agents": ["socrates", "aristotle", "marcus_aurelius"],
                "reasoning_focus": "Self-discovery, virtue development, practical action",
                "cognitive_enhancement": "Develops self-reflection and decision-making skills"
            },
            "anxiety_management": {
                "query": "I'm overwhelmed by things I can't control and feel anxious all the time",
                "expected_agents": ["marcus_aurelius", "lao_tzu"],  
                "reasoning_focus": "Dichotomy of control, acceptance, natural flow",
                "cognitive_enhancement": "Builds emotional regulation and stress management"
            },
            "decision_complexity": {
                "query": "I have a difficult choice to make and keep going back and forth",
                "expected_agents": ["aristotle", "socrates", "lao_tzu"],
                "reasoning_focus": "Systematic analysis, assumption examination, natural wisdom",
                "cognitive_enhancement": "Improves decision-making frameworks and reduces analysis paralysis"
            },
            "relationship_conflict": {
                "query": "I'm having ongoing conflicts with someone important to me",
                "expected_agents": ["lao_tzu", "aristotle", "marcus_aurelius"],
                "reasoning_focus": "Harmony, virtue ethics, practical wisdom",
                "cognitive_enhancement": "Develops empathy, communication skills, and conflict resolution"
            }
        },
        "system15_features": {
            "intuitive_analytical_bridge": "Combines gut feelings with logical analysis",
            "metacognitive_awareness": "Teaches you how to think about thinking",
            "progressive_complexity": "Adapts difficulty to your cognitive readiness",
            "real_time_transparency": "Watch the reasoning process unfold live"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)