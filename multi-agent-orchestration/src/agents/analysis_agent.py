"""
Analysis Agent - Agent B
Responsible for analyzing and summarizing information gathered by the Research Agent.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing and summarizing research data."""
    
    def __init__(
        self,
        name: str = "Analysis Agent",
        model: str = "gpt-4",
        temperature: float = 0.5,  # Balanced temperature for analysis
    ):
        super().__init__(name, model, temperature)
        self.analysis_cache: Dict[str, Any] = {}
    
    def get_system_prompt(self) -> str:
        return """
        You are an Analysis Agent specialized in processing, analyzing, and synthesizing information.
        
        Your capabilities include:
        - Data analysis and pattern recognition
        - Information synthesis and summarization
        - Critical evaluation of sources and claims
        - Trend identification and insights extraction
        - Comparative analysis across multiple sources
        - Risk and opportunity assessment
        
        Your tasks:
        1. Analyze research data for key insights and patterns
        2. Synthesize information from multiple sources
        3. Evaluate credibility and reliability of information
        4. Identify trends, correlations, and anomalies
        5. Generate actionable insights and recommendations
        6. Provide structured analysis reports
        
        Always be objective, thorough, and evidence-based in your analysis.
        Clearly distinguish between facts, interpretations, and assumptions.
        Highlight uncertainties and data limitations.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and analyze research data."""
        research_data = input_data.get("research_data", {})
        analysis_type = input_data.get("analysis_type", "comprehensive")
        focus_areas = input_data.get("focus_areas", [])
        
        # Debug: Print what we received
        print(f"📊 Analysis Debug - Received research_data keys: {list(research_data.keys()) if research_data else 'None'}")
        if research_data:
            content_items = research_data.get('content_gathered', [])
            print(f"📊 Analysis Debug - Content items: {len(content_items)}")
            for i, item in enumerate(content_items[:3]):  # Show first 3 items
                print(f"  Item {i+1}: {item.get('type', 'unknown')} - {len(item.get('content', ''))} chars")
        
        # Check if we have actual content to analyze
        content_items = research_data.get('content_gathered', []) if research_data else []
        has_content = any(item.get('content') and len(item.get('content', '').strip()) > 0 
                         for item in content_items)
        
        if not research_data:
            return {
                "error": "No research data provided for analysis",
                "status": "failed"
            }
        
        # If no actual content but we have a query, analyze based on the query itself
        if not has_content and research_data.get('query'):
            print("🔄 No scraped content available, generating analysis based on query knowledge")
            return await self._analyze_from_query(research_data.get('query'), analysis_type)
        
        analysis_results = {
            "analysis_type": analysis_type,
            "input_summary": self._summarize_input_data(research_data),
            "key_insights": [],
            "patterns_identified": [],
            "source_evaluation": {},
            "synthesis": "",
            "recommendations": [],
            "confidence_scores": {},
            "limitations": [],
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # 1. Evaluate sources
            analysis_results["source_evaluation"] = await self._evaluate_sources(research_data)
            
            # 2. Extract key insights
            analysis_results["key_insights"] = await self._extract_key_insights(
                research_data, focus_areas
            )
            
            # 3. Identify patterns
            analysis_results["patterns_identified"] = await self._identify_patterns(research_data)
            
            # 4. Synthesize information
            analysis_results["synthesis"] = await self._synthesize_information(
                research_data, analysis_type
            )
            
            # 5. Generate recommendations
            analysis_results["recommendations"] = await self._generate_recommendations(
                research_data, analysis_results["key_insights"]
            )
            
            # 6. Assess confidence and limitations
            analysis_results["confidence_scores"] = await self._assess_confidence(research_data)
            analysis_results["limitations"] = await self._identify_limitations(research_data)
            
            # Cache results
            cache_key = f"{analysis_type}_{hash(str(research_data))}"
            self.analysis_cache[cache_key] = analysis_results
            
        except Exception as e:
            analysis_results["status"] = "failed"
            analysis_results["error"] = str(e)
        
        return analysis_results
    
    def _summarize_input_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of input data for tracking."""
        return {
            "query": research_data.get("query", ""),
            "sources_count": len(research_data.get("sources_researched", [])),
            "content_items": len(research_data.get("content_gathered", [])),
            "search_results_count": len(research_data.get("search_results", [])),
            "has_recommendations": bool(research_data.get("recommendations", []))
        }
    
    async def _evaluate_sources(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the credibility and reliability of sources."""
        sources = research_data.get("sources_researched", [])
        content_gathered = research_data.get("content_gathered", [])
        
        if not sources and not content_gathered:
            return {"evaluation": "No sources to evaluate"}
        
        messages = [{
            "role": "user",
            "content": f"""
            Evaluate the following sources for credibility, reliability, and potential bias:
            
            Sources: {json.dumps(sources, indent=2)}
            
            Content gathered: {json.dumps([{
                "url": item.get("url", ""),
                "type": item.get("type", ""),
                "title": item.get("title", "")[:100] if item.get("title") else ""
            } for item in content_gathered], indent=2)}
            
            For each source, provide:
            1. Credibility assessment (High/Medium/Low)
            2. Potential bias indicators
            3. Source type (academic, news, blog, official, etc.)
            4. Reliability factors
            5. Any red flags or concerns
            
            Format as structured JSON.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            # Try to parse as JSON, fallback to text analysis
            return json.loads(response)
        except json.JSONDecodeError:
            return {"evaluation": response, "format": "text"}
    
    async def _extract_key_insights(
        self,
        research_data: Dict[str, Any],
        focus_areas: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract key insights from research data."""
        content_text = self._extract_content_text(research_data)
        
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\nFocus particularly on these areas: {', '.join(focus_areas)}"
        
        messages = [{
            "role": "user",
            "content": f"""
            Analyze the following research content and extract key insights:
            
            Research Query: {research_data.get('query', '')}
            
            Content:
            {content_text}
            {focus_instruction}
            
            Extract 5-7 key insights that:
            1. Directly relate to the research query
            2. Represent important findings or conclusions
            3. Are supported by evidence in the content
            4. Provide actionable information
            5. Highlight significant trends or patterns
            
            For each insight, provide:
            - The insight statement
            - Supporting evidence
            - Confidence level (High/Medium/Low)
            - Relevance score (1-10)
            
            Format as a JSON array of objects.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            insights = json.loads(response)
            return insights if isinstance(insights, list) else [insights]
        except json.JSONDecodeError:
            # Fallback to parsing text response
            return [{"insight": response, "confidence": "medium", "relevance": 7}]
    
    async def _identify_patterns(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify patterns and trends in the research data."""
        content_text = self._extract_content_text(research_data)
        
        messages = [{
            "role": "user",
            "content": f"""
            Analyze the following content to identify patterns, trends, and relationships:
            
            {content_text}
            
            Look for:
            1. Recurring themes or topics
            2. Temporal trends or changes over time
            3. Correlations between different data points
            4. Contradictions or conflicting information
            5. Data gaps or missing information
            6. Cause-and-effect relationships
            
            For each pattern, provide:
            - Pattern description
            - Evidence or examples
            - Strength of pattern (Strong/Moderate/Weak)
            - Implications or significance
            
            Format as a JSON array.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            patterns = json.loads(response)
            return patterns if isinstance(patterns, list) else [patterns]
        except json.JSONDecodeError:
            return [{"pattern": response, "strength": "moderate"}]
    
    async def _synthesize_information(
        self,
        research_data: Dict[str, Any],
        analysis_type: str
    ) -> str:
        """Synthesize all information into a coherent analysis."""
        content_text = self._extract_content_text(research_data)
        summary = research_data.get("summary", "")
        
        synthesis_instructions = {
            "comprehensive": "Provide a thorough, detailed synthesis covering all aspects",
            "executive": "Focus on high-level findings and strategic implications",
            "technical": "Emphasize technical details, methodologies, and data analysis",
            "comparative": "Compare and contrast different sources and viewpoints",
            "critical": "Critically evaluate claims, identify weaknesses and strengths"
        }
        
        instruction = synthesis_instructions.get(analysis_type, synthesis_instructions["comprehensive"])
        
        messages = [{
            "role": "user",
            "content": f"""
            Synthesize the following research information into a coherent analysis:
            
            Research Query: {research_data.get('query', '')}
            
            Research Summary: {summary}
            
            Content: {content_text}
            
            Analysis Type: {analysis_type}
            Instructions: {instruction}
            
            Provide a well-structured synthesis that:
            1. Integrates information from all sources
            2. Addresses the original research query
            3. Presents findings in logical order
            4. Distinguishes between confirmed facts and interpretations
            5. Acknowledges uncertainties and limitations
            6. Draws meaningful conclusions
            
            Structure with clear headings and sections.
            """
        }]
        
        synthesis = await self.invoke_llm(messages)
        return synthesis
    
    async def _generate_recommendations(
        self,
        research_data: Dict[str, Any],
        key_insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analysis."""
        insights_text = json.dumps(key_insights, indent=2)
        
        messages = [{
            "role": "user",
            "content": f"""
            Based on the research analysis and key insights, generate actionable recommendations:
            
            Research Query: {research_data.get('query', '')}
            
            Key Insights: {insights_text}
            
            Generate 3-5 specific, actionable recommendations that:
            1. Address the research query or problem
            2. Are based on evidence from the analysis
            3. Are feasible and practical to implement
            4. Have clear expected outcomes
            5. Consider potential risks or challenges
            
            For each recommendation, provide:
            - Recommendation statement
            - Rationale/justification
            - Expected impact (High/Medium/Low)
            - Implementation difficulty (Easy/Medium/Hard)
            - Risk level (Low/Medium/High)
            - Timeline for implementation
            
            Format as a JSON array.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        try:
            recommendations = json.loads(response)
            return recommendations if isinstance(recommendations, list) else [recommendations]
        except json.JSONDecodeError:
            return [{"recommendation": response, "impact": "medium", "difficulty": "medium"}]
    
    async def _assess_confidence(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess confidence levels in different aspects of the analysis."""
        return {
            "overall_confidence": self._calculate_overall_confidence(research_data),
            "source_reliability": self._assess_source_reliability(research_data),
            "data_completeness": self._assess_data_completeness(research_data),
            "analysis_depth": "medium",  # Self-assessment
        }
    
    def _calculate_overall_confidence(self, research_data: Dict[str, Any]) -> str:
        """Calculate overall confidence in the analysis."""
        source_count = len(research_data.get("sources_researched", []))
        content_count = len(research_data.get("content_gathered", []))
        
        if source_count >= 3 and content_count >= 3:
            return "high"
        elif source_count >= 2 or content_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _assess_source_reliability(self, research_data: Dict[str, Any]) -> str:
        """Assess the reliability of sources used."""
        content_gathered = research_data.get("content_gathered", [])
        error_count = sum(1 for item in content_gathered if item.get("type") == "error")
        
        if error_count == 0 and len(content_gathered) > 0:
            return "high"
        elif error_count < len(content_gathered) / 2:
            return "medium"
        else:
            return "low"
    
    def _assess_data_completeness(self, research_data: Dict[str, Any]) -> str:
        """Assess completeness of the research data."""
        has_content = bool(research_data.get("content_gathered"))
        has_summary = bool(research_data.get("summary"))
        has_search = bool(research_data.get("search_results"))
        
        completeness_score = sum([has_content, has_summary, has_search])
        
        if completeness_score >= 3:
            return "high"
        elif completeness_score >= 2:
            return "medium"
        else:
            return "low"
    
    async def _identify_limitations(self, research_data: Dict[str, Any]) -> List[str]:
        """Identify limitations in the research and analysis."""
        limitations = []
        
        # Check for common limitations
        source_count = len(research_data.get("sources_researched", []))
        if source_count < 3:
            limitations.append(f"Limited number of sources ({source_count})")
        
        content_errors = sum(1 for item in research_data.get("content_gathered", []) if item.get("type") == "error")
        if content_errors > 0:
            limitations.append(f"Failed to access {content_errors} sources")
        
        if not research_data.get("search_results"):
            limitations.append("No historical data search performed")
        
        # Use LLM to identify additional limitations
        content_text = self._extract_content_text(research_data)[:1000]  # Truncate for analysis
        
        messages = [{
            "role": "user",
            "content": f"""
            Identify potential limitations in this research analysis:
            
            Research Query: {research_data.get('query', '')}
            Content Sample: {content_text}
            Source Count: {source_count}
            
            Identify limitations such as:
            - Data quality issues
            - Scope limitations
            - Bias potential
            - Temporal constraints
            - Methodology limitations
            
            List 2-3 key limitations concisely.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        # Parse limitations from response
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                limitations.append(line[1:].strip())
            elif line and len(line) > 10 and not line.endswith(':'):
                limitations.append(line)
        
        return limitations[:5]  # Limit to 5 key limitations
    
    async def _analyze_from_query(self, query: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate analysis based on query alone when no scraped content is available."""
        prompt = f"""
        Analyze the following query and provide insights based on your knowledge: "{query}"
        
        Please provide:
        1. Key insights related to this topic (3-5 insights)
        2. Current trends and patterns
        3. Important considerations
        4. Recommendations for action
        5. Confidence level for each insight (high/medium/low)
        
        Focus on factual, current information while acknowledging any limitations due to knowledge cutoff.
        Format your response as a structured analysis.
        """
        
        try:
            response = await self.invoke_llm([{"role": "user", "content": prompt}])
            
            # Parse the response into structured format
            insights = self._parse_insights_from_text(response)
            recommendations = self._parse_recommendations_from_text(response)
            
            return {
                "analysis_type": analysis_type,
                "input_summary": {"query": query, "method": "knowledge_based"},
                "key_insights": insights,
                "patterns_identified": ["Knowledge-based analysis due to limited scraped data"],
                "source_evaluation": {"method": "LLM knowledge", "reliability": "medium"},
                "synthesis": response,
                "recommendations": recommendations,
                "confidence_scores": {"overall": "medium", "note": "Based on training data knowledge"},
                "limitations": ["Limited to training data", "No real-time web data", "Cannot verify current status"],
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to analyze query: {str(e)}",
                "status": "failed",
                "query": query
            }
    
    def _parse_insights_from_text(self, text: str) -> List[str]:
        """Extract insights from LLM response text."""
        insights = []
        lines = text.split('\n')
        in_insights_section = False
        
        for line in lines:
            line = line.strip()
            if 'insight' in line.lower() and ':' in line:
                in_insights_section = True
                continue
            elif in_insights_section and line:
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*')):
                    insight = line[2:].strip() if line[1:2] == '.' else line[1:].strip()
                    if insight:
                        insights.append(insight)
                elif line.startswith(('recommendation', 'consider', 'important')):
                    break
        
        return insights[:5]  # Limit to 5 insights
    
    def _parse_recommendations_from_text(self, text: str) -> List[str]:
        """Extract recommendations from LLM response text."""
        recommendations = []
        lines = text.split('\n')
        in_recommendations_section = False
        
        for line in lines:
            line = line.strip()
            if 'recommendation' in line.lower() and ':' in line:
                in_recommendations_section = True
                continue
            elif in_recommendations_section and line:
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*')):
                    rec = line[2:].strip() if line[1:2] == '.' else line[1:].strip()
                    if rec:
                        recommendations.append(rec)
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _extract_content_text(self, research_data: Dict[str, Any]) -> str:
        """Extract text content from research data for analysis."""
        content_parts = []
        
        # Add summary if available
        if research_data.get("summary"):
            content_parts.append("SUMMARY:\n" + research_data["summary"])
        
        # Add content from gathered sources
        for item in research_data.get("content_gathered", []):
            if item.get("type") in ["scraped", "fetched"] and item.get("content"):
                source_info = f"SOURCE ({item.get('url', 'unknown')}):\n"
                if item.get("title"):
                    source_info += f"Title: {item['title']}\n"
                source_info += item["content"]
                content_parts.append(source_info)
        
        return "\n\n---\n\n".join(content_parts)
    
    def get_capabilities(self) -> List[str]:
        """Return list of analysis agent capabilities."""
        base_capabilities = super().get_capabilities()
        analysis_capabilities = [
            "data_analysis",
            "pattern_recognition",
            "information_synthesis",
            "source_evaluation",
            "insight_extraction",
            "recommendation_generation",
            "confidence_assessment"
        ]
        return base_capabilities + analysis_capabilities
    
    def get_analysis_cache(self) -> Dict[str, Any]:
        """Return current analysis cache."""
        return self.analysis_cache
    
    def clear_analysis_cache(self):
        """Clear analysis cache."""
        self.analysis_cache = {}