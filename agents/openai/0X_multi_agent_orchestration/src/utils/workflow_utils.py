"""
Utility functions for the multi-agent orchestration system.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class WorkflowTimer:
    """Timer utility for tracking workflow execution time."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.step_times: Dict[str, float] = {}
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
    
    def end(self):
        """End the timer."""
        self.end_time = time.time()
    
    def step_start(self, step_name: str):
        """Start timing a specific step."""
        self.step_times[f"{step_name}_start"] = time.time()
    
    def step_end(self, step_name: str):
        """End timing a specific step."""
        if f"{step_name}_start" in self.step_times:
            start_time = self.step_times[f"{step_name}_start"]
            self.step_times[f"{step_name}_duration"] = time.time() - start_time
    
    def get_total_duration(self) -> float:
        """Get total execution duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def get_step_duration(self, step_name: str) -> float:
        """Get duration of a specific step."""
        return self.step_times.get(f"{step_name}_duration", 0.0)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get timing summary."""
        return {
            "total_duration": self.get_total_duration(),
            "step_durations": {
                step.replace("_duration", ""): duration
                for step, duration in self.step_times.items()
                if step.endswith("_duration")
            }
        }

class WorkflowValidator:
    """Validator for workflow inputs and outputs."""
    
    @staticmethod
    def validate_query(query: str) -> Dict[str, Any]:
        """Validate user query."""
        issues = []
        
        if not query or not query.strip():
            issues.append("Query cannot be empty")
        
        if len(query.strip()) < 5:
            issues.append("Query too short (minimum 5 characters)")
        
        if len(query) > 1000:
            issues.append("Query too long (maximum 1000 characters)")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "query_length": len(query),
            "word_count": len(query.split()) if query else 0
        }
    
    @staticmethod
    def validate_user_input(user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user input structure."""
        issues = []
        
        # Check URLs if provided
        urls = user_input.get("urls", [])
        if urls and not isinstance(urls, list):
            issues.append("URLs must be a list")
        
        # Check search terms if provided
        search_terms = user_input.get("search_terms", [])
        if search_terms and not isinstance(search_terms, list):
            issues.append("Search terms must be a list")
        
        # Check max sources
        max_sources = user_input.get("max_sources", 5)
        if not isinstance(max_sources, int) or max_sources < 1 or max_sources > 20:
            issues.append("Max sources must be an integer between 1 and 20")
        
        # Check objectives
        objectives = user_input.get("objectives", [])
        if objectives and not isinstance(objectives, list):
            issues.append("Objectives must be a list")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "input_keys": list(user_input.keys())
        }
    
    @staticmethod
    def validate_workflow_output(output: Dict[str, Any]) -> Dict[str, Any]:
        """Validate workflow output completeness."""
        issues = []
        required_keys = [
            "query",
            "research_summary",
            "key_insights",
            "strategic_recommendations",
            "action_plan",
            "next_steps"
        ]
        
        for key in required_keys:
            if key not in output:
                issues.append(f"Missing required output key: {key}")
        
        # Check content quality
        if "key_insights" in output and len(output["key_insights"]) == 0:
            issues.append("No key insights generated")
        
        if "strategic_recommendations" in output and len(output["strategic_recommendations"]) == 0:
            issues.append("No strategic recommendations generated")
        
        if "action_plan" in output and len(output["action_plan"]) == 0:
            issues.append("No action plan generated")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "completeness_score": (len(required_keys) - len([i for i in issues if "Missing required" in i])) / len(required_keys)
        }

class ResultsFormatter:
    """Formatter for workflow results."""
    
    @staticmethod
    def format_for_display(results: Dict[str, Any]) -> str:
        """Format results for human-readable display."""
        output = []
        
        # Header
        output.append("=" * 60)
        output.append("MULTI-AGENT ORCHESTRATION RESULTS")
        output.append("=" * 60)
        
        # Query
        output.append(f"\n🎯 ORIGINAL QUERY:")
        output.append(f"{results.get('query', 'N/A')}")
        
        # Research Summary
        output.append(f"\n🔍 RESEARCH SUMMARY:")
        output.append(f"{results.get('research_summary', 'No research summary available')}")
        
        # Key Insights
        insights = results.get('key_insights', [])
        if insights:
            output.append(f"\n💡 KEY INSIGHTS ({len(insights)}):")
            for i, insight in enumerate(insights, 1):
                insight_text = insight if isinstance(insight, str) else insight.get('insight', str(insight))
                output.append(f"{i}. {insight_text}")
        
        # Strategic Recommendations
        recommendations = results.get('strategic_recommendations', [])
        if recommendations:
            output.append(f"\n📋 STRATEGIC RECOMMENDATIONS ({len(recommendations)}):")
            for i, rec in enumerate(recommendations, 1):
                output.append(f"{i}. {rec}")
        
        # Action Plan
        action_plan = results.get('action_plan', [])
        if action_plan:
            output.append(f"\n🎯 PRIORITY ACTIONS ({len(action_plan)}):")
            for i, action in enumerate(action_plan, 1):
                title = action.get('title', f'Action {i}')
                priority = action.get('priority', 'medium')
                output.append(f"{i}. [{priority.upper()}] {title}")
                if action.get('description'):
                    output.append(f"   {action['description'][:100]}...")
        
        # Next Steps
        next_steps = results.get('next_steps', [])
        if next_steps:
            output.append(f"\n⏭️ IMMEDIATE NEXT STEPS:")
            for i, step in enumerate(next_steps, 1):
                step_text = step if isinstance(step, str) else step.get('action', str(step))
                output.append(f"{i}. {step_text}")
        
        # Metadata
        metadata = results.get('workflow_metadata', {})
        if metadata:
            output.append(f"\n📊 EXECUTION METADATA:")
            output.append(f"Duration: {metadata.get('duration_seconds', 0):.2f} seconds")
            output.append(f"Steps: {' → '.join(metadata.get('agents_used', []))}")
            output.append(f"Retries: {metadata.get('retry_count', 0)}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
    
    @staticmethod
    def format_for_json(results: Dict[str, Any]) -> str:
        """Format results as JSON."""
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_summary(results: Dict[str, Any]) -> str:
        """Format a brief summary of results."""
        insights_count = len(results.get('key_insights', []))
        recommendations_count = len(results.get('strategic_recommendations', []))
        actions_count = len(results.get('action_plan', []))
        
        metadata = results.get('workflow_metadata', {})
        duration = metadata.get('duration_seconds', 0)
        
        return f"""
📋 EXECUTION SUMMARY:
• Query: {results.get('query', 'N/A')[:50]}...
• Insights Generated: {insights_count}
• Recommendations: {recommendations_count}
• Priority Actions: {actions_count}
• Execution Time: {duration:.2f}s
• Success: {'✅' if insights_count > 0 and recommendations_count > 0 else '❌'}
        """.strip()

class WorkflowCache:
    """Cache system for workflow results."""
    
    def __init__(self, cache_dir: str = ".workflow_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, query: str, user_input: Dict[str, Any]) -> str:
        """Generate cache key for query and input."""
        import hashlib
        cache_content = f"{query}_{json.dumps(user_input, sort_keys=True)}"
        return hashlib.md5(cache_content.encode()).hexdigest()
    
    def get(self, query: str, user_input: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached results if available."""
        cache_key = self._get_cache_key(query, user_input)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid (24 hours)
                cached_time = datetime.fromisoformat(cached_data.get('timestamp', ''))
                if datetime.now() - cached_time < timedelta(hours=24):
                    return cached_data.get('results')
            except (json.JSONDecodeError, ValueError, KeyError):
                # Invalid cache file, remove it
                cache_file.unlink(missing_ok=True)
        
        return None
    
    def set(self, query: str, user_input: Dict[str, Any], results: Dict[str, Any]):
        """Cache workflow results."""
        cache_key = self._get_cache_key(query, user_input)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        cache_data = {
            "query": query,
            "user_input": user_input,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to cache results: {e}")
    
    def clear(self):
        """Clear all cached results."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "cached_results": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "cache_directory": str(self.cache_dir)
        }

async def run_with_timeout(
    coro: Callable,
    timeout_seconds: int = 300,
    timeout_message: str = "Operation timed out"
) -> Any:
    """Run an async operation with timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        raise TimeoutError(f"{timeout_message} (timeout: {timeout_seconds}s)")

def safe_json_loads(json_str: str, fallback: Any = None) -> Any:
    """Safely parse JSON string with fallback."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return fallback

def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def extract_urls_from_text(text: str) -> List[str]:
    """Extract URLs from text using regex."""
    import re
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    return re.findall(url_pattern, text)

def calculate_confidence_score(
    research_quality: float,
    analysis_depth: float,
    action_completeness: float
) -> Dict[str, Any]:
    """Calculate overall confidence score for workflow results."""
    weights = {
        "research": 0.3,
        "analysis": 0.4,
        "action": 0.3
    }
    
    overall_score = (
        research_quality * weights["research"] +
        analysis_depth * weights["analysis"] +
        action_completeness * weights["action"]
    )
    
    confidence_level = "low"
    if overall_score >= 0.8:
        confidence_level = "high"
    elif overall_score >= 0.6:
        confidence_level = "medium"
    
    return {
        "overall_score": overall_score,
        "confidence_level": confidence_level,
        "component_scores": {
            "research_quality": research_quality,
            "analysis_depth": analysis_depth,
            "action_completeness": action_completeness
        },
        "weights": weights
    }