# wisdom_coordinator.py
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List, AsyncGenerator
from datetime import datetime
from ollama import Client
import os

from tools.llm_powered_agents import (
    PhilosophicalAgentFactory,
    MetacognitiveReflector,
    DialogicalChallenger
)

logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
client = Client(host=OLLAMA_HOST)

class System15Controller:
    """Implements the revolutionary System 1.5 metacognitive framework"""
    
    def __init__(self):
        self.cognitive_load_threshold = 0.7
        self.complexity_levels = ["simple", "moderate", "complex", "advanced"]
    
    async def analyze_cognitive_load(self, query: str) -> Dict[str, Any]:
        """Assess cognitive complexity and user readiness"""
        analysis_prompt = f"""
Analyze the cognitive load and complexity of this query:
"{query}"

Rate on scales of 0.0-1.0:
- emotional_intensity: How emotionally charged is this?
- conceptual_complexity: How many abstract concepts are involved?
- decision_urgency: How time-sensitive is this?
- ambiguity_level: How unclear or vague is this?
- personal_stakes: How significant is this to the person's life?

Return JSON:
{{
    "overall_load": 0.0-1.0,
    "emotional_intensity": 0.0-1.0,
    "conceptual_complexity": 0.0-1.0,
    "decision_urgency": 0.0-1.0,
    "ambiguity_level": 0.0-1.0,
    "personal_stakes": 0.0-1.0,
    "recommended_approach": "gentle|standard|intensive",
    "suggested_agents": ["agent1", "agent2"],
    "pacing_recommendation": "slow|normal|rapid"
}}
"""
        
        try:
            messages = [{"role": "user", "content": analysis_prompt}]
            response = await self._call_ollama(messages, temperature=0.3)
            
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback analysis
        return {
            "overall_load": 0.5,
            "emotional_intensity": 0.5,
            "conceptual_complexity": 0.5,
            "decision_urgency": 0.3,
            "ambiguity_level": 0.4,
            "personal_stakes": 0.6,
            "recommended_approach": "standard",
            "suggested_agents": ["socrates", "marcus"],
            "pacing_recommendation": "normal"
        }
    
    async def _call_ollama(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Async Ollama API wrapper"""
        def sync_call():
            options = {"temperature": temperature, "num_predict": 800}
            resp = client.chat(model=OLLAMA_MODEL, messages=messages, options=options)
            if isinstance(resp, dict):
                return resp.get("message", {}).get("content", "")
            return getattr(resp.message, "content", "")
        
        return await asyncio.to_thread(sync_call)

class AdvancedAgentOrchestrator:
    """Intelligent orchestration of multiple philosophical agents"""
    
    def __init__(self):
        self.agent_factory = PhilosophicalAgentFactory()
        self.collaboration_patterns = {
            "sequential": self._sequential_reasoning,
            "parallel": self._parallel_reasoning,
            "hierarchical": self._hierarchical_reasoning,
            "dialectical": self._dialectical_reasoning
        }
    
    async def select_optimal_agents(self, query: str, cognitive_analysis: Dict) -> Dict[str, Any]:
        """AI-powered intelligent agent selection"""
        selection_prompt = f"""
You are an expert AI coordinator selecting philosophical agents for optimal wisdom generation.

QUERY: "{query}"
COGNITIVE_ANALYSIS: {json.dumps(cognitive_analysis, indent=2)}

AGENT CAPABILITIES:
- SOCRATES: Assumption examination, definitional clarity, epistemic inquiry, revealing contradictions
- MARCUS AURELIUS: Anxiety management, control dichotomy, control resilience building, practical action
- LAO TZU: Flow states, natural solutions, balance, reducing resistance and force
- ARISTOTLE: Systematic analysis, habit formation, virtue development, golden mean

SELECTION CRITERIA:
1. Emotional tone → Agent fit (anxiety→Marcus, confusion→Socrates, forcing→Lao Tzu, analysis→Aristotle)
2. Problem complexity → Number of agents (simple=2, complex=3-4)
3. User readiness → Depth level (gentle/standard/intensive)
4. Complementary perspectives → Avoid redundancy, ensure diverse viewpoints

Return JSON:
{{
    "selected_agents": ["agent1", "agent2", "agent3"],
    "primary_agent": "most_relevant_agent",
    "collaboration_pattern": "sequential|parallel|hierarchical|dialectical",
    "reasoning_depth": "surface|moderate|deep|profound",
    "selection_rationale": "detailed explanation of choices",
    "expected_synergies": ["how agents complement each other"]
}}
Make sure "selected_agents" is a list of strings only, using lowercase names like "socrates", "marcus", "laotzu", "aristotle".
"""
        
        try:
            messages = [{"role": "user", "content": selection_prompt}]
            response = await self._call_ollama(messages, temperature=0.4)
            
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except Exception as e:
            logger.error(f"Agent selection failed: {e}")
        
        # Fallback selection using heuristics
        return self._heuristic_agent_selection(query, cognitive_analysis)
    
    def _heuristic_agent_selection(self, query: str, cognitive_analysis: Dict) -> Dict[str, Any]:
        """Fallback heuristic-based agent selection"""
        selected = []
        q_lower = query.lower()
        
        # Emotional state mapping
        if cognitive_analysis.get("emotional_intensity", 0) > 0.6:
            selected.append("marcus")
        
        # Confusion/clarity needs
        if any(word in q_lower for word in ["confused", "unclear", "don't understand", "what is"]):
            selected.append("socrates")
        
        # Flow/resistance issues
        if any(word in q_lower for word in ["stuck", "forcing", "struggle", "balance"]):
            selected.append("laotzu")
        
        # Analysis/decision needs
        if any(word in q_lower for word in ["decision", "analyze", "plan", "habit"]):
            selected.append("aristotle")
        
        # Ensure minimum 2 agents
        if len(selected) < 2:
            selected.extend(["socrates", "marcus"])
        
        return {
            "selected_agents": selected[:3],
            "primary_agent": selected[0] if selected else "socrates",
            "collaboration_pattern": "parallel",
            "reasoning_depth": "moderate",
            "selection_rationale": "Heuristic-based selection using keyword and emotional analysis",
            "expected_synergies": ["Diverse philosophical perspectives"]
        }
    
    async def _call_ollama(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Async Ollama API wrapper"""
        def sync_call():
            options = {"temperature": temperature, "num_predict": 1000}
            resp = client.chat(model=OLLAMA_MODEL, messages=messages, options=options)
            if isinstance(resp, dict):
                return resp.get("message", {}).get("content", "")
            return getattr(resp.message, "content", "")
        
        return await asyncio.to_thread(sync_call)
    
    async def _sequential_reasoning(self, agents: List, query: str, context: Dict) -> List[Dict]:
        """Sequential reasoning where each agent builds on previous insights"""
        reasoning_chain = []
        accumulated_context = context.copy()
        
        for i, agent in enumerate(agents):
            step_context = {
                **accumulated_context,
                "previous_insights": reasoning_chain,
                "position_in_sequence": i + 1,
                "total_agents": len(agents)
            }
            
            reasoning_step = await agent.generate_reasoning_step(query, step_context)
            reasoning_chain.append(reasoning_step)
            
            # Add this insight to context for next agent
            accumulated_context[f"insight_from_{agent.philosopher_name}"] = reasoning_step.get("core_insight", "")
        
        return reasoning_chain
    
    async def _parallel_reasoning(self, agents: List, query: str, context: Dict) -> List[Dict]:
        """Parallel reasoning where agents work independently"""
        tasks = []
        for agent in agents:
            agent_context = {
                **context,
                "collaboration_mode": "independent",
                "other_agents": [a.philosopher_name for a in agents if a != agent]
            }
            tasks.append(agent.generate_reasoning_step(query, agent_context))
        
        return await asyncio.gather(*tasks)
    
    async def _hierarchical_reasoning(self, agents: List, query: str, context: Dict) -> List[Dict]:
        """Hierarchical reasoning with primary agent leading"""
        primary_agent = agents[0]
        secondary_agents = agents[1:]
        
        # Primary agent provides foundational reasoning
        primary_reasoning = await primary_agent.generate_reasoning_step(query, {
            **context,
            "role": "primary_reasoner",
            "responsibility": "provide_foundation"
        })
        
        # Secondary agents elaborate and refine
        secondary_tasks = []
        for agent in secondary_agents:
            agent_context = {
                **context,
                "primary_reasoning": primary_reasoning,
                "role": "secondary_elaborator"
            }
            secondary_tasks.append(agent.generate_reasoning_step(query, agent_context))
        
        secondary_reasoning = await asyncio.gather(*secondary_tasks)
        
        return [primary_reasoning] + secondary_reasoning
    
    async def _dialectical_reasoning(self, agents: List, query: str, context: Dict) -> List[Dict]:
        """Dialectical reasoning with agents challenging each other"""
        if len(agents) < 2:
            return await self._parallel_reasoning(agents, query, context)
        
        # First round: initial positions
        initial_reasoning = await self._parallel_reasoning(agents, query, {
            **context,
            "dialectical_round": 1,
            "instruction": "present_your_perspective"
        })
        
        # Second round: cross-validation and synthesis
        validation_tasks = []
        for i, agent in enumerate(agents):
            other_reasoning = [r for j, r in enumerate(initial_reasoning) if j != i]
            validation_context = {
                **context,
                "dialectical_round": 2,
                "peer_reasoning": other_reasoning,
                "instruction": "validate_and_synthesize"
            }
            validation_tasks.append(agent.validate_peer_reasoning(other_reasoning[0] if other_reasoning else {}))
        
        validations = await asyncio.gather(*validation_tasks)
        
        # Combine initial reasoning with validations
        dialectical_chain = []
        for i, (reasoning, validation) in enumerate(zip(initial_reasoning, validations)):
            dialectical_step = {
                **reasoning,
                "peer_validation": validation,
                "dialectical_synthesis": validation.get("synthesis_suggestion", "")
            }
            dialectical_chain.append(dialectical_step)
        
        return dialectical_chain

class ReasoningSynthesizer:
    """Advanced synthesis engine for multi-agent reasoning"""
    
    def __init__(self):
        self.metacognitive_reflector = MetacognitiveReflector()
        self.dialectical_challenger = DialogicalChallenger()
    
    async def generate_comprehensive_synthesis(self, 
                                            query: str, 
                                            reasoning_chain: List[Dict],
                                            agent_selection: Dict,
                                            cognitive_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive synthesis with metacognitive enhancement"""
        
        synthesis_prompt = f"""
You are a master synthesizer creating transformative wisdom from multiple philosophical perspectives.

ORIGINAL QUERY: "{query}"

REASONING CHAIN:
{json.dumps(reasoning_chain, indent=2)}

AGENT SELECTION RATIONALE:
{json.dumps(agent_selection, indent=2)}

COGNITIVE ANALYSIS:
{json.dumps(cognitive_analysis, indent=2)}

Create a comprehensive synthesis as JSON:
{{
    "integrated_wisdom": "unified insight combining all perspectives",
    "key_insights": ["most important discoveries"],
    "practical_steps": ["specific actionable guidance"],
    "metacognitive_enhancement": "how this process improves thinking skills",
    "reasoning_quality_assessment": "evaluation of the reasoning process",
    "cognitive_bridges": ["connections between different thinking modes"],
    "transformative_elements": ["aspects that could change user's perspective"],
    "application_scenarios": ["where this wisdom applies"],
    "deepening_questions": ["questions for continued exploration"]
}}
"""
        
        try:
            messages = [{"role": "user", "content": synthesis_prompt}]
            response = await self._call_ollama(messages, temperature=0.8, max_tokens=1500)
            
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                base_synthesis = json.loads(response[json_start:json_end])
            else:
                base_synthesis = self._create_fallback_synthesis(reasoning_chain)
        except Exception as e:
            logger.error(f"Synthesis generation failed: {e}")
            base_synthesis = self._create_fallback_synthesis(reasoning_chain)
        
        # Enhance with metacognitive prompts
        metacognitive_prompts = await self.metacognitive_reflector.generate_metacognitive_prompts(reasoning_chain)
        
        # Add dialectical challenges
        dialectical_challenges = await self.dialectical_challenger.generate_counter_perspectives(base_synthesis)
        
        # Combine all synthesis elements
        enhanced_synthesis = {
            **base_synthesis,
            "metacognitive_prompts": metacognitive_prompts,
            "dialectical_challenges": dialectical_challenges,
            "synthesis_quality_score": self._calculate_synthesis_quality(base_synthesis, reasoning_chain),
            "cognitive_enhancement_elements": self._identify_cognitive_enhancements(reasoning_chain)
        }
        
        return enhanced_synthesis
    
    def _create_fallback_synthesis(self, reasoning_chain: List[Dict]) -> Dict[str, Any]:
        """Create basic synthesis when AI synthesis fails"""
        philosophers = [step.get("philosopher", "Unknown") for step in reasoning_chain]
        insights = [step.get("core_insight", "") for step in reasoning_chain]
        
        return {
            "integrated_wisdom": "Multiple philosophical perspectives offer complementary wisdom for addressing your concern.",
            "key_insights": insights[:3],
            "practical_steps": ["Reflect on each perspective", "Choose the most resonant approach", "Take small action steps"],
            "metacognitive_enhancement": "This multi-perspective analysis enhances your ability to see complex issues from different angles",
            "reasoning_quality_assessment": "Good diversity of perspectives provided",
            "cognitive_bridges": ["Connecting intuitive and analytical thinking"],
            "transformative_elements": ["Exposure to different philosophical frameworks"],
            "application_scenarios": ["Similar complex decisions", "Future philosophical inquiries"],
            "deepening_questions": ["Which perspective resonates most?", "How might you combine these approaches?"]
        }
    
    def _calculate_synthesis_quality(self, synthesis: Dict, reasoning_chain: List[Dict]) -> float:
        """Calculate quality score for synthesis"""
        score = 0.0
        
        # Check for key elements
        if synthesis.get("integrated_wisdom"): score += 0.2
        if synthesis.get("key_insights") and len(synthesis["key_insights"]) >= 2: score += 0.2
        if synthesis.get("practical_steps"): score += 0.2
        if synthesis.get("metacognitive_enhancement"): score += 0.2
        if len(reasoning_chain) >= 2: score += 0.2  # Multi-perspective bonus
        
        return min(score, 1.0)
    
    def _identify_cognitive_enhancements(self, reasoning_chain: List[Dict]) -> List[str]:
        """Identify cognitive enhancement elements in the reasoning"""
        enhancements = []
        
        reasoning_types = [step.get("reasoning_type", "") for step in reasoning_chain]
        if "analytical" in reasoning_types and "intuitive" in reasoning_types:
            enhancements.append("System 1.5 integration: bridging intuitive and analytical thinking")
        
        if len(set(step.get("philosopher", "") for step in reasoning_chain)) >= 3:
            enhancements.append("Multi-perspective analysis: developing cognitive flexibility")
        
        if any("socratic_catalyst" in step for step in reasoning_chain):
            enhancements.append("Socratic questioning: improving inquiry skills")
        
        if any("metacognitive_awareness" in step for step in reasoning_chain):
            enhancements.append("Metacognitive development: thinking about thinking")
        
        return enhancements
    
    async def _call_ollama(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Async Ollama API wrapper"""
        def sync_call():
            options = {"temperature": temperature, "num_predict": max_tokens}
            resp = client.chat(model=OLLAMA_MODEL, messages=messages, options=options)
            if isinstance(resp, dict):
                return resp.get("message", {}).get("content", "")
            return getattr(resp.message, "content", "")
        
        return await asyncio.to_thread(sync_call)

class AdvancedWisdomCoordinator:
    """Revolutionary System 1.5 Metacognitive Reasoning Coordinator"""
    
    def __init__(self):
        self.system15_controller = System15Controller()
        self.orchestrator = AdvancedAgentOrchestrator()
        self.synthesizer = ReasoningSynthesizer()
        self.reasoning_cache = {}
        
    def _normalize_agent_name(self, a: Any) -> str:
        known_agents = {'socrates', 'marcus', 'laotzu', 'aristotle', 'marcusaurelius', 'lao-tzu'}
        if isinstance(a, str):
            return a.lower().replace(' ', '').replace('-', '')
        if isinstance(a, dict):
            for key, value in a.items():
                lkey = key.lower().replace(' ', '').replace('-', '')
                if lkey in known_agents:
                    return lkey
                if isinstance(value, str):
                    lval = value.lower().replace(' ', '').replace('-', '')
                    if lval in known_agents:
                        return lval
            return list(a.keys())[0] if a.keys() else 'unknown'
        return str(a)
    
    async def process_wisdom_request(self, query: str, context: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream real-time reasoning steps to the user"""
        try:
            # Step 1: Cognitive Load Analysis
            yield {
                "step": "cognitive_analysis",
                "status": "processing",
                "message": "Analyzing cognitive complexity and emotional context...",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            cognitive_analysis = await self.system15_controller.analyze_cognitive_load(query)
            
            yield {
                "step": "cognitive_analysis",
                "status": "complete",
                "data": cognitive_analysis,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Step 2: Agent Selection
            yield {
                "step": "agent_selection",
                "status": "processing",
                "message": "Selecting optimal philosophical agents for your inquiry...",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            agent_selection = await self.orchestrator.select_optimal_agents(query, cognitive_analysis)
            
            yield {
                "step": "agent_selection", 
                "status": "complete",
                "data": agent_selection,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Normalize selected_agents to ensure they are strings
            agent_selection["selected_agents"] = [self._normalize_agent_name(a) for a in agent_selection["selected_agents"]]
            
            # Step 3: Multi-Agent Reasoning
            yield {
                "step": "reasoning_initiation",
                "status": "processing", 
                "message": f"Consulting the council of wisdom: {', '.join(agent_selection['selected_agents'])}...",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Create agent instances
            agents = []
            for agent_name in agent_selection["selected_agents"]:
                try:
                    agent = PhilosophicalAgentFactory.create_agent(agent_name)
                    agents.append(agent)
                except Exception as e:
                    logger.error(f"Failed to create agent {agent_name}: {e}")
                    continue
            
            # Execute collaboration pattern
            collaboration_pattern = agent_selection.get("collaboration_pattern", "parallel")
            reasoning_context = {
                **(context or {}),
                "cognitive_analysis": cognitive_analysis,
                "agent_selection": agent_selection
            }
            
            if collaboration_pattern == "sequential":
                reasoning_chain = await self.orchestrator._sequential_reasoning(agents, query, reasoning_context)
            elif collaboration_pattern == "hierarchical":
                reasoning_chain = await self.orchestrator._hierarchical_reasoning(agents, query, reasoning_context)
            elif collaboration_pattern == "dialectical":
                reasoning_chain = await self.orchestrator._dialectical_reasoning(agents, query, reasoning_context)
            else:
                reasoning_chain = await self.orchestrator._parallel_reasoning(agents, query, reasoning_context)
            
            # Stream individual reasoning steps
            for i, reasoning_step in enumerate(reasoning_chain):
                yield {
                    "step": "reasoning_step",
                    "status": "complete",
                    "step_number": i + 1,
                    "total_steps": len(reasoning_chain),
                    "data": reasoning_step,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Small delay for better UX streaming effect
                await asyncio.sleep(0.1)
            
            # Step 4: Synthesis Generation
            yield {
                "step": "synthesis",
                "status": "processing",
                "message": "Synthesizing wisdom and generating metacognitive insights...",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            synthesis = await self.synthesizer.generate_comprehensive_synthesis(
                query, reasoning_chain, agent_selection, cognitive_analysis
            )
            
            yield {
                "step": "synthesis",
                "status": "complete", 
                "data": synthesis,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Step 5: Final Integration
            yield {
                "step": "integration_complete",
                "status": "complete",
                "message": "Wisdom council has completed its deliberation",
                "final_result": {
                    "query": query,
                    "cognitive_analysis": cognitive_analysis,
                    "agent_selection": agent_selection,
                    "reasoning_chain": reasoning_chain,
                    "synthesis": synthesis,
                    "philosophers_consulted": [agent.philosopher_name for agent in agents],
                    "system_version": "AAIRS 2.0 - System 1.5 Framework",
                    "processing_quality": "revolutionary_metacognitive_enhancement"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.exception("Error in wisdom processing stream")
            yield {
                "step": "error",
                "status": "error",
                "message": f"Wisdom processing encountered an error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def ask_wisdom(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Complete wisdom processing (non-streaming version)"""
        final_result = None
        
        async for step in self.process_wisdom_request(query, context):
            if step.get("step") == "integration_complete":
                final_result = step["final_result"]
                break
        
        return final_result or {
            "error": "Processing failed",
            "query": query,
            "timestamp": datetime.utcnow().isoformat()
        }