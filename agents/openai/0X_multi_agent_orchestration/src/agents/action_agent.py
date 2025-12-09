"""
Action Agent - Agent C
Responsible for deciding next steps and producing final results based on analysis.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_agent import BaseAgent


class ActionPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionType(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    IMPLEMENTATION = "implementation"
    COMMUNICATION = "communication"
    MONITORING = "monitoring"
    VALIDATION = "validation"

class ActionAgent(BaseAgent):
    """Agent responsible for decision-making and action planning based on analysis."""
    
    def __init__(
        self,
        name: str = "Action Agent",
        model: str = "gpt-4",
        temperature: float = 0.4,  # Balanced for strategic thinking
    ):
        super().__init__(name, model, temperature)
        self.action_history: List[Dict[str, Any]] = []
        self.pending_actions: List[Dict[str, Any]] = []
    
    def get_system_prompt(self) -> str:
        return """
        You are an Action Agent specialized in strategic decision-making and action planning.
        
        Your capabilities include:
        - Strategic analysis and decision-making
        - Action plan development and prioritization
        - Risk assessment and mitigation planning
        - Resource allocation and timeline planning
        - Success metrics definition
        - Implementation roadmap creation
        
        Your tasks:
        1. Analyze research and analysis results to identify required actions
        2. Develop comprehensive action plans with clear steps
        3. Prioritize actions based on impact, urgency, and resources
        4. Define success criteria and measurement approaches
        5. Identify risks and develop mitigation strategies
        6. Create implementation timelines and milestones
        7. Provide clear, actionable final recommendations
        
        Always be strategic, practical, and results-oriented.
        Focus on actions that directly address the original objectives.
        Consider implementation feasibility and resource constraints.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis results and generate action plan."""
        analysis_data = input_data.get("analysis_data", {})
        research_data = input_data.get("research_data", {})
        original_query = input_data.get("original_query", "")
        constraints = input_data.get("constraints", {})
        objectives = input_data.get("objectives", [])
        
        if not analysis_data and not research_data:
            return {
                "error": "No analysis or research data provided",
                "status": "failed"
            }
        
        action_results = {
            "original_query": original_query,
            "input_summary": self._summarize_inputs(analysis_data, research_data),
            "strategic_assessment": {},
            "action_plan": [],
            "priority_actions": [],
            "implementation_roadmap": {},
            "success_metrics": [],
            "risk_assessment": {},
            "resource_requirements": {},
            "final_recommendations": [],
            "next_steps": [],
            "status": "completed",
            "execution_score": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # 1. Strategic assessment
            action_results["strategic_assessment"] = await self._conduct_strategic_assessment(
                analysis_data, research_data, original_query
            )
            
            # 2. Generate comprehensive action plan
            action_results["action_plan"] = await self._generate_action_plan(
                analysis_data, objectives, constraints
            )
            
            # 3. Prioritize actions
            action_results["priority_actions"] = await self._prioritize_actions(
                action_results["action_plan"]
            )
            
            # 4. Create implementation roadmap
            action_results["implementation_roadmap"] = await self._create_implementation_roadmap(
                action_results["priority_actions"]
            )
            
            # 5. Define success metrics
            action_results["success_metrics"] = await self._define_success_metrics(
                original_query, objectives, action_results["action_plan"]
            )
            
            # 6. Assess risks
            action_results["risk_assessment"] = await self._assess_risks(
                action_results["action_plan"], constraints
            )
            
            # 7. Determine resource requirements
            action_results["resource_requirements"] = await self._determine_resource_requirements(
                action_results["action_plan"]
            )
            
            # 8. Generate final recommendations
            action_results["final_recommendations"] = await self._generate_final_recommendations(
                action_results
            )
            
            # 9. Define immediate next steps
            action_results["next_steps"] = self._define_next_steps(
                action_results["priority_actions"]
            )
            
            # 10. Calculate execution score
            action_results["execution_score"] = self._calculate_execution_score(action_results)
            
            # Store in action history
            self.action_history.append(action_results)
            
        except Exception as e:
            action_results["status"] = "failed"
            action_results["error"] = str(e)
        
        return action_results
    
    def _summarize_inputs(
        self,
        analysis_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Summarize input data for processing overview."""
        return {
            "has_analysis": bool(analysis_data),
            "has_research": bool(research_data),
            "key_insights_count": len(analysis_data.get("key_insights", [])),
            "recommendations_count": len(analysis_data.get("recommendations", [])),
            "sources_researched": len(research_data.get("sources_researched", [])),
            "analysis_confidence": analysis_data.get("confidence_scores", {}).get("overall_confidence", "unknown")
        }
    
    async def _conduct_strategic_assessment(
        self,
        analysis_data: Dict[str, Any],
        research_data: Dict[str, Any],
        original_query: str
    ) -> Dict[str, Any]:
        """Conduct strategic assessment of the situation."""
        analysis_summary = analysis_data.get("synthesis", "")
        key_insights = json.dumps(analysis_data.get("key_insights", []), indent=2)
        recommendations = json.dumps(analysis_data.get("recommendations", []), indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Conduct a strategic assessment based on the following information:
            
            Original Query: {original_query}
            
            Analysis Summary: {analysis_summary}
            
            Key Insights: {key_insights}
            
            Existing Recommendations: {recommendations}
            
            Provide a strategic assessment covering:
            1. Current situation analysis
            2. Key opportunities identified
            3. Major challenges or obstacles
            4. Strategic priorities
            5. Critical success factors
            6. Competitive/environmental factors
            
            Format as structured JSON with clear sections.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"assessment": response, "format": "text"}
    
    async def _generate_action_plan(
        self,
        analysis_data: Dict[str, Any],
        objectives: List[str],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate comprehensive action plan."""
        insights = json.dumps(analysis_data.get("key_insights", []), indent=2)
        recommendations = json.dumps(analysis_data.get("recommendations", []), indent=2)
        
        objectives_text = "\n".join([f"- {obj}" for obj in objectives]) if objectives else "Not specified"
        constraints_text = json.dumps(constraints, indent=2) if constraints else "None specified"
        
        messages = [{
            "role": "user",
            "content": f"""
            Generate a comprehensive action plan based on:
            
            Key Insights: {insights}
            
            Recommendations: {recommendations}
            
            Objectives: {objectives_text}
            
            Constraints: {constraints_text}
            
            Create 5-8 specific actions that:
            1. Address the key insights and recommendations
            2. Align with stated objectives
            3. Consider the given constraints
            4. Are specific and measurable
            5. Have clear deliverables
            
            For each action, provide:
            - Action title and description
            - Type (research/analysis/implementation/communication/monitoring)
            - Priority (critical/high/medium/low)
            - Estimated effort (hours or days)
            - Dependencies
            - Expected outcomes
            - Success criteria
            
            Format as a JSON array of action objects.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            actions = json.loads(response)
            return actions if isinstance(actions, list) else [actions]
        except json.JSONDecodeError:
            # Fallback parsing
            return [{
                "title": "Primary Action",
                "description": response,
                "type": "implementation",
                "priority": "high"
            }]
    
    async def _prioritize_actions(self, action_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize actions based on impact, urgency, and dependencies."""
        if not action_plan:
            return []
        
        # Sort by priority and add priority scores
        priority_scores = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }
        
        prioritized_actions = []
        for action in action_plan:
            action_copy = action.copy()
            priority = action.get("priority", "medium").lower()
            action_copy["priority_score"] = priority_scores.get(priority, 2)
            
            # Add urgency assessment
            action_copy["urgency_assessment"] = await self._assess_action_urgency(action)
            
            prioritized_actions.append(action_copy)
        
        # Sort by priority score (descending) then by urgency
        prioritized_actions.sort(
            key=lambda x: (x["priority_score"], x.get("urgency_assessment", {}).get("urgency_score", 0)),
            reverse=True
        )
        
        return prioritized_actions[:5]  # Return top 5 priority actions
    
    async def _assess_action_urgency(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Assess urgency of an individual action."""
        action_text = json.dumps(action, indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Assess the urgency of this action:
            
            {action_text}
            
            Consider:
            1. Time sensitivity
            2. Dependencies on other actions
            3. External deadlines or constraints
            4. Risk of delay
            5. Impact on overall success
            
            Provide urgency assessment with:
            - Urgency level (immediate/soon/moderate/flexible)
            - Urgency score (1-10)
            - Key urgency factors
            
            Format as JSON.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "urgency_level": "moderate",
                "urgency_score": 5,
                "factors": [response[:100]]
            }
    
    async def _create_implementation_roadmap(
        self,
        priority_actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create implementation roadmap with timeline."""
        if not priority_actions:
            return {"phases": [], "timeline": "Not determined"}
        
        actions_text = json.dumps(priority_actions, indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Create an implementation roadmap for these priority actions:
            
            {actions_text}
            
            Organize into phases considering:
            1. Dependencies between actions
            2. Resource requirements
            3. Logical sequence
            4. Risk management
            5. Quick wins vs long-term initiatives
            
            Provide:
            - Implementation phases (3-4 phases max)
            - Timeline estimates for each phase
            - Parallel vs sequential activities
            - Key milestones
            - Critical path identification
            
            Format as structured JSON.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "phases": ["Phase 1: Planning", "Phase 2: Implementation", "Phase 3: Review"],
                "timeline": response,
                "format": "text"
            }
    
    async def _define_success_metrics(
        self,
        original_query: str,
        objectives: List[str],
        action_plan: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Define success metrics and KPIs."""
        objectives_text = "\n".join([f"- {obj}" for obj in objectives]) if objectives else "General success"
        actions_summary = "\n".join([f"- {action.get('title', '')}" for action in action_plan])
        
        messages = [{
            "role": "user",
            "content": f"""
            Define success metrics for this initiative:
            
            Original Query: {original_query}
            
            Objectives: {objectives_text}
            
            Planned Actions: {actions_summary}
            
            Create 3-5 success metrics that are:
            1. Specific and measurable
            2. Aligned with objectives
            3. Achievable and realistic
            4. Time-bound
            5. Relevant to the outcomes
            
            For each metric, provide:
            - Metric name and description
            - Measurement method
            - Target value or threshold
            - Timeline for achievement
            - Importance level (critical/important/nice-to-have)
            
            Format as JSON array.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            metrics = json.loads(response)
            return metrics if isinstance(metrics, list) else [metrics]
        except json.JSONDecodeError:
            return [{
                "name": "Overall Success",
                "description": response,
                "importance": "critical"
            }]
    
    async def _assess_risks(
        self,
        action_plan: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess risks and develop mitigation strategies."""
        actions_text = json.dumps(action_plan, indent=2)
        constraints_text = json.dumps(constraints, indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Assess risks for this action plan:
            
            Actions: {actions_text}
            
            Constraints: {constraints_text}
            
            Identify and analyze:
            1. Implementation risks
            2. Resource risks
            3. Timeline risks
            4. Quality risks
            5. External risks
            
            For each risk category, provide:
            - Risk description
            - Probability (High/Medium/Low)
            - Impact (High/Medium/Low)
            - Mitigation strategies
            - Contingency plans
            
            Format as structured JSON.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"risk_assessment": response, "format": "text"}
    
    async def _determine_resource_requirements(
        self,
        action_plan: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Determine resource requirements for implementation."""
        actions_text = json.dumps(action_plan, indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Determine resource requirements for these actions:
            
            {actions_text}
            
            Analyze requirements for:
            1. Human resources (roles, skills, time)
            2. Technology resources (tools, systems, infrastructure)
            3. Financial resources (budget estimates)
            4. Information resources (data, research, expertise)
            5. External resources (vendors, consultants, partners)
            
            Provide structured breakdown with estimates.
            Format as JSON.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"resources": response, "format": "text"}
    
    async def _generate_final_recommendations(self, action_results: Dict[str, Any]) -> List[str]:
        """Generate final strategic recommendations."""
        # Summarize key components
        strategic_assessment = action_results.get("strategic_assessment", {})
        priority_actions = action_results.get("priority_actions", [])
        risk_assessment = action_results.get("risk_assessment", {})
        
        context = {
            "strategic_assessment": strategic_assessment,
            "top_actions": priority_actions[:3],  # Top 3 actions
            "key_risks": risk_assessment
        }
        
        messages = [{
            "role": "user",
            "content": f"""
            Generate final strategic recommendations based on this analysis:
            
            {json.dumps(context, indent=2)}
            
            Provide 3-5 final recommendations that:
            1. Synthesize all analysis and planning
            2. Focus on highest-impact actions
            3. Address key risks and constraints
            4. Are actionable and specific
            5. Align with strategic objectives
            
            Make each recommendation concise but comprehensive.
            Format as a list of recommendation statements.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        # Parse recommendations from response
        recommendations = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                recommendations.append(line[1:].strip())
            elif line and len(line) > 20 and not line.endswith(':'):
                recommendations.append(line)
        
        return recommendations[:5]  # Limit to 5 key recommendations
    
    def _define_next_steps(self, priority_actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Define immediate next steps from priority actions."""
        next_steps = []
        
        for i, action in enumerate(priority_actions[:3]):  # Top 3 actions
            next_step = {
                "step": i + 1,
                "action": action.get("title", f"Action {i+1}"),
                "description": action.get("description", "")[:200],
                "timeline": "Immediate" if i == 0 else f"{(i+1)*7} days",
                "responsible": "Implementation team",
                "deliverable": action.get("expected_outcomes", ["Action completion"])[0] if action.get("expected_outcomes") else "Completed action"
            }
            next_steps.append(next_step)
        
        return next_steps
    
    def _calculate_execution_score(self, action_results: Dict[str, Any]) -> int:
        """Calculate execution readiness score (0-100)."""
        score = 0
        
        # Action plan quality (0-30)
        action_count = len(action_results.get("action_plan", []))
        score += min(30, action_count * 5)
        
        # Strategic assessment completeness (0-20)
        if action_results.get("strategic_assessment"):
            score += 20
        
        # Risk assessment (0-20)
        if action_results.get("risk_assessment"):
            score += 20
        
        # Success metrics defined (0-15)
        metrics_count = len(action_results.get("success_metrics", []))
        score += min(15, metrics_count * 3)
        
        # Resource requirements (0-15)
        if action_results.get("resource_requirements"):
            score += 15
        
        return min(100, score)
    
    def get_capabilities(self) -> List[str]:
        """Return list of action agent capabilities."""
        base_capabilities = super().get_capabilities()
        action_capabilities = [
            "strategic_planning",
            "action_prioritization",
            "risk_assessment",
            "resource_planning",
            "implementation_roadmapping",
            "success_metrics_definition",
            "decision_making"
        ]
        return base_capabilities + action_capabilities
    
    def get_action_history(self) -> List[Dict[str, Any]]:
        """Return action history."""
        return self.action_history
    
    def get_pending_actions(self) -> List[Dict[str, Any]]:
        """Return pending actions."""
        return self.pending_actions
    
    def add_pending_action(self, action: Dict[str, Any]):
        """Add action to pending list."""
        action["added_timestamp"] = datetime.now().isoformat()
        self.pending_actions.append(action)
    
    def complete_pending_action(self, action_id: str) -> bool:
        """Mark pending action as completed."""
        for i, action in enumerate(self.pending_actions):
            if action.get("id") == action_id:
                completed_action = self.pending_actions.pop(i)
                completed_action["completed_timestamp"] = datetime.now().isoformat()
                self.action_history.append(completed_action)
                return True
        return False