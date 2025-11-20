"""
Multi-Agent Orchestrator using LangGraph.
Coordinates between Research, Analysis, and Action agents.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ..agents.action_agent import ActionAgent
from ..agents.analysis_agent import AnalysisAgent
from ..agents.research_agent import ResearchAgent


# Define the state structure for the orchestrator
class OrchestratorState(TypedDict):
    """State structure for the multi-agent orchestrator."""
    # Input
    original_query: str
    user_input: Dict[str, Any]
    
    # Processing state
    current_step: str
    step_history: List[str]
    
    # Agent outputs
    research_results: Optional[Dict[str, Any]]
    analysis_results: Optional[Dict[str, Any]]
    action_results: Optional[Dict[str, Any]]
    
    # Control flow
    next_agent: Optional[str]
    retry_count: int
    max_retries: int
    
    # Final output
    final_output: Optional[Dict[str, Any]]
    execution_summary: Optional[Dict[str, Any]]
    
    # Metadata
    start_time: str
    end_time: Optional[str]
    total_duration: Optional[float]

class MultiAgentOrchestrator:
    """LangGraph-based orchestrator for multi-agent workflows."""
    
    def __init__(
        self,
        research_agent: Optional[ResearchAgent] = None,
        analysis_agent: Optional[AnalysisAgent] = None,
        action_agent: Optional[ActionAgent] = None,
        mcp_base_url: str = "http://localhost:8000"
    ):
        # Initialize agents
        self.research_agent = research_agent or ResearchAgent(mcp_base_url=mcp_base_url)
        self.analysis_agent = analysis_agent or AnalysisAgent()
        self.action_agent = action_agent or ActionAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
        # Execution history
        self.execution_history: List[Dict[str, Any]] = []
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes for each agent
        workflow.add_node("research", self._research_node)
        workflow.add_node("analysis", self._analysis_node)
        workflow.add_node("action", self._action_node)
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("finalizer", self._finalizer_node)
        
        # Define the workflow edges
        workflow.set_entry_point("coordinator")
        
        # Coordinator decides which agent to call first
        workflow.add_conditional_edges(
            "coordinator",
            self._route_from_coordinator,
            {
                "research": "research",
                "analysis": "analysis",
                "action": "action",
                "end": "finalizer"
            }
        )
        
        # After research, go to analysis or coordinator
        workflow.add_conditional_edges(
            "research",
            self._route_from_research,
            {
                "analysis": "analysis",
                "coordinator": "coordinator",
                "end": "finalizer"
            }
        )
        
        # After analysis, go to action or coordinator
        workflow.add_conditional_edges(
            "analysis",
            self._route_from_analysis,
            {
                "action": "action",
                "coordinator": "coordinator",
                "end": "finalizer"
            }
        )
        
        # After action, usually finalize
        workflow.add_conditional_edges(
            "action",
            self._route_from_action,
            {
                "coordinator": "coordinator",
                "end": "finalizer"
            }
        )
        
        # Finalizer ends the workflow
        workflow.add_edge("finalizer", END)
        
        return workflow
    
    async def _research_node(self, state: OrchestratorState) -> OrchestratorState:
        """Execute research agent."""
        print(f"🔍 Executing Research Agent...")
        
        try:
            # Prepare input for research agent
            research_input = self._prepare_research_input(state)
            
            # Execute research
            research_results = await self.research_agent.process(research_input)
            
            # Update state
            state["research_results"] = research_results
            state["current_step"] = "research_completed"
            state["step_history"].append("research")
            
            print(f"✅ Research completed: {len(research_results.get('content_gathered', []))} sources processed")
            
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            state["research_results"] = {"error": str(e), "status": "failed"}
            state["current_step"] = "research_failed"
        
        return state
    
    async def _analysis_node(self, state: OrchestratorState) -> OrchestratorState:
        """Execute analysis agent."""
        print(f"📊 Executing Analysis Agent...")
        
        try:
            # Prepare input for analysis agent
            analysis_input = self._prepare_analysis_input(state)
            
            # Execute analysis
            analysis_results = await self.analysis_agent.process(analysis_input)
            
            # Update state
            state["analysis_results"] = analysis_results
            state["current_step"] = "analysis_completed"
            state["step_history"].append("analysis")
            
            print(f"✅ Analysis completed: {len(analysis_results.get('key_insights', []))} insights identified")
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            state["analysis_results"] = {"error": str(e), "status": "failed"}
            state["current_step"] = "analysis_failed"
        
        return state
    
    async def _action_node(self, state: OrchestratorState) -> OrchestratorState:
        """Execute action agent."""
        print(f"🎯 Executing Action Agent...")
        
        try:
            # Prepare input for action agent
            action_input = self._prepare_action_input(state)
            
            # Execute action planning
            action_results = await self.action_agent.process(action_input)
            
            # Update state
            state["action_results"] = action_results
            state["current_step"] = "action_completed"
            state["step_history"].append("action")
            
            print(f"✅ Action planning completed: {len(action_results.get('action_plan', []))} actions planned")
            
        except Exception as e:
            print(f"❌ Action planning failed: {str(e)}")
            state["action_results"] = {"error": str(e), "status": "failed"}
            state["current_step"] = "action_failed"
        
        return state
    
    async def _coordinator_node(self, state: OrchestratorState) -> OrchestratorState:
        """Coordinate the workflow and decide next steps."""
        print(f"🎭 Orchestrator coordination step...")
        
        # Determine next agent based on current state
        current_step = state.get("current_step", "start")
        step_history = state.get("step_history", [])
        
        # Logic for determining next agent
        if current_step == "start":
            state["next_agent"] = "research"
        elif current_step == "research_completed" and "analysis" not in step_history:
            state["next_agent"] = "analysis"
        elif current_step == "analysis_completed" and "action" not in step_history:
            state["next_agent"] = "action"
        elif current_step in ["research_failed", "analysis_failed", "action_failed"]:
            # Handle retries
            retry_count = state.get("retry_count", 0)
            max_retries = state.get("max_retries", 2)
            
            if retry_count < max_retries:
                state["retry_count"] = retry_count + 1
                # Retry the failed step
                if current_step == "research_failed":
                    state["next_agent"] = "research"
                elif current_step == "analysis_failed":
                    state["next_agent"] = "analysis"
                elif current_step == "action_failed":
                    state["next_agent"] = "action"
            else:
                state["next_agent"] = "end"
        else:
            state["next_agent"] = "end"
        
        state["current_step"] = "coordinated"
        print(f"🎯 Next agent: {state['next_agent']}")
        
        return state
    
    async def _finalizer_node(self, state: OrchestratorState) -> OrchestratorState:
        """Finalize the workflow and prepare output."""
        print(f"🏁 Finalizing workflow...")
        
        # Calculate duration
        start_time = datetime.fromisoformat(state["start_time"])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        state["end_time"] = end_time.isoformat()
        state["total_duration"] = duration
        
        # Prepare final output
        final_output = self._prepare_final_output(state)
        state["final_output"] = final_output
        
        # Create execution summary
        execution_summary = self._create_execution_summary(state)
        state["execution_summary"] = execution_summary
        
        # Store in history
        self.execution_history.append({
            "query": state["original_query"],
            "duration": duration,
            "steps_executed": state["step_history"],
            "success": self._determine_success(state),
            "timestamp": end_time.isoformat()
        })
        
        print(f"✅ Workflow completed in {duration:.2f} seconds")
        
        return state
    
    def _route_from_coordinator(self, state: OrchestratorState) -> str:
        """Route from coordinator to appropriate agent."""
        return state.get("next_agent", "end")
    
    def _route_from_research(self, state: OrchestratorState) -> str:
        """Route from research agent."""
        if state.get("research_results", {}).get("status") == "failed":
            return "coordinator"  # Let coordinator handle retry logic
        return "analysis"
    
    def _route_from_analysis(self, state: OrchestratorState) -> str:
        """Route from analysis agent."""
        if state.get("analysis_results", {}).get("status") == "failed":
            return "coordinator"  # Let coordinator handle retry logic
        return "action"
    
    def _route_from_action(self, state: OrchestratorState) -> str:
        """Route from action agent."""
        return "end"  # Action is usually the final step
    
    def _prepare_research_input(self, state: OrchestratorState) -> Dict[str, Any]:
        """Prepare input for research agent."""
        user_input = state.get("user_input", {})
        
        return {
            "query": state["original_query"],
            "urls": user_input.get("urls", []),
            "search_terms": user_input.get("search_terms", []),
            "max_sources": user_input.get("max_sources", 5)
        }
    
    def _prepare_analysis_input(self, state: OrchestratorState) -> Dict[str, Any]:
        """Prepare input for analysis agent."""
        user_input = state.get("user_input", {})
        
        return {
            "research_data": state.get("research_results", {}),
            "analysis_type": user_input.get("analysis_type", "comprehensive"),
            "focus_areas": user_input.get("focus_areas", [])
        }
    
    def _prepare_action_input(self, state: OrchestratorState) -> Dict[str, Any]:
        """Prepare input for action agent."""
        user_input = state.get("user_input", {})
        
        return {
            "analysis_data": state.get("analysis_results", {}),
            "research_data": state.get("research_results", {}),
            "original_query": state["original_query"],
            "constraints": user_input.get("constraints", {}),
            "objectives": user_input.get("objectives", [])
        }
    
    def _prepare_final_output(self, state: OrchestratorState) -> Dict[str, Any]:
        """Prepare the final comprehensive output."""
        return {
            "query": state["original_query"],
            "research_summary": self._extract_research_summary(state),
            "key_insights": self._extract_key_insights(state),
            "strategic_recommendations": self._extract_recommendations(state),
            "action_plan": self._extract_action_plan(state),
            "next_steps": self._extract_next_steps(state),
            "confidence_assessment": self._extract_confidence_assessment(state),
            "workflow_metadata": {
                "steps_executed": state["step_history"],
                "duration_seconds": state.get("total_duration", 0),
                "agents_used": list(set(state["step_history"])),
                "retry_count": state.get("retry_count", 0)
            }
        }
    
    def _create_execution_summary(self, state: OrchestratorState) -> Dict[str, Any]:
        """Create execution summary for the workflow."""
        return {
            "total_steps": len(state["step_history"]),
            "successful_steps": len([s for s in state["step_history"] if s in ["research", "analysis", "action"]]),
            "failed_steps": state.get("retry_count", 0),
            "execution_path": " → ".join(state["step_history"]),
            "performance_metrics": {
                "total_duration": state.get("total_duration", 0),
                "average_step_duration": state.get("total_duration", 0) / max(len(state["step_history"]), 1),
                "research_sources": len(state.get("research_results", {}).get("sources_researched", [])),
                "insights_generated": len(state.get("analysis_results", {}).get("key_insights", [])),
                "actions_planned": len(state.get("action_results", {}).get("action_plan", []))
            }
        }
    
    def _extract_research_summary(self, state: OrchestratorState) -> str:
        """Extract research summary from state."""
        research_results = state.get("research_results", {})
        return research_results.get("summary", "No research summary available")
    
    def _extract_key_insights(self, state: OrchestratorState) -> List[Dict[str, Any]]:
        """Extract key insights from analysis results."""
        analysis_results = state.get("analysis_results", {})
        return analysis_results.get("key_insights", [])
    
    def _extract_recommendations(self, state: OrchestratorState) -> List[str]:
        """Extract recommendations from action results."""
        action_results = state.get("action_results", {})
        return action_results.get("final_recommendations", [])
    
    def _extract_action_plan(self, state: OrchestratorState) -> List[Dict[str, Any]]:
        """Extract action plan from action results."""
        action_results = state.get("action_results", {})
        return action_results.get("priority_actions", [])
    
    def _extract_next_steps(self, state: OrchestratorState) -> List[Dict[str, Any]]:
        """Extract next steps from action results."""
        action_results = state.get("action_results", {})
        return action_results.get("next_steps", [])
    
    def _extract_confidence_assessment(self, state: OrchestratorState) -> Dict[str, Any]:
        """Extract confidence assessment from analysis results."""
        analysis_results = state.get("analysis_results", {})
        return analysis_results.get("confidence_scores", {})
    
    def _determine_success(self, state: OrchestratorState) -> bool:
        """Determine if the workflow was successful."""
        # Check if all required steps completed successfully
        required_steps = ["research", "analysis", "action"]
        step_history = state.get("step_history", [])
        
        # All required steps must be in history
        steps_completed = all(step in step_history for step in required_steps)
        
        # No major failures
        no_final_failures = (
            state.get("research_results", {}).get("status") != "failed" and
            state.get("analysis_results", {}).get("status") != "failed" and
            state.get("action_results", {}).get("status") != "failed"
        )
        
        return steps_completed and no_final_failures
    
    async def execute(
        self,
        query: str,
        user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute the multi-agent workflow."""
        print(f"🚀 Starting multi-agent orchestration for: {query}")
        
        # Initialize state
        initial_state = OrchestratorState(
            original_query=query,
            user_input=user_input or {},
            current_step="start",
            step_history=[],
            research_results=None,
            analysis_results=None,
            action_results=None,
            next_agent=None,
            retry_count=0,
            max_retries=2,
            final_output=None,
            execution_summary=None,
            start_time=datetime.now().isoformat(),
            end_time=None,
            total_duration=None
        )
        
        # Execute the workflow
        final_state = await self.app.ainvoke(initial_state)
        
        return final_state["final_output"]
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.execution_history
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "research_agent": self.research_agent.get_status(),
            "analysis_agent": self.analysis_agent.get_status(),
            "action_agent": self.action_agent.get_status()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the orchestrator and all agents."""
        try:
            # Check MCP server connection
            from ..mcp_server.client import MCPClient
            async with MCPClient() as mcp_client:
                mcp_health = await mcp_client.health_check()
            
            return {
                "orchestrator": "healthy",
                "agents": self.get_agent_status(),
                "mcp_server": mcp_health,
                "execution_history_count": len(self.execution_history),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "orchestrator": "healthy",
                "agents": self.get_agent_status(),
                "mcp_server": f"error: {str(e)}",
                "execution_history_count": len(self.execution_history),
                "timestamp": datetime.now().isoformat()
            }