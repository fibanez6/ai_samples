"""
Configuration management for the multi-agent orchestration system.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables
load_dotenv()

class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""
    api_key: str = Field(default="demo-key", description="OpenAI API key")
    model: str = Field(default="gpt-4", description="OpenAI model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for responses")
    max_tokens: Optional[int] = Field(default=4000, description="Maximum tokens in response")
    timeout: int = Field(default=60, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or not v.startswith('sk-'):
            raise ValueError('Invalid OpenAI API key format')
        return v

class MCPServerConfig(BaseModel):
    """MCP Server configuration."""
    base_url: str = Field(default="http://localhost:8000", description="MCP server base URL")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    health_check_interval: int = Field(default=60, description="Health check interval in seconds")

class AgentConfig(BaseModel):
    """Individual agent configuration."""
    name: str = Field(..., description="Agent name")
    model: str = Field(default="gpt-4", description="Model to use for this agent")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for this agent")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens for this agent")
    timeout: int = Field(default=60, description="Timeout for this agent")

class OrchestratorConfig(BaseModel):
    """Orchestrator configuration."""
    max_retries: int = Field(default=2, description="Maximum retry attempts per agent")
    timeout_per_agent: int = Field(default=300, description="Timeout per agent in seconds")
    parallel_execution: bool = Field(default=False, description="Enable parallel agent execution")
    cache_enabled: bool = Field(default=True, description="Enable result caching")
    cache_ttl_hours: int = Field(default=24, description="Cache TTL in hours")

class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field(default="INFO", description="Logging level")
    file_logging: bool = Field(default=True, description="Enable file logging")
    log_file: str = Field(default="orchestrator.log", description="Log file name")
    max_file_size_mb: int = Field(default=10, description="Maximum log file size in MB")
    backup_count: int = Field(default=5, description="Number of backup log files")

class SecurityConfig(BaseModel):
    """Security configuration."""
    rate_limit_requests_per_minute: int = Field(default=60, description="Rate limit per minute")
    allowed_domains: List[str] = Field(default=[], description="Allowed domains for fetching")
    blocked_domains: List[str] = Field(default=[], description="Blocked domains")
    max_content_size_mb: int = Field(default=10, description="Maximum content size in MB")
    enable_content_filtering: bool = Field(default=True, description="Enable content filtering")

class DatabaseConfig(BaseModel):
    """Database configuration."""
    db_path: str = Field(default="mcp_data.db", description="SQLite database path")
    connection_pool_size: int = Field(default=5, description="Connection pool size")
    query_timeout: int = Field(default=30, description="Query timeout in seconds")
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_interval_hours: int = Field(default=24, description="Backup interval in hours")

class MultiAgentConfig(BaseModel):
    """Complete multi-agent system configuration."""
    
    # Core configurations
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    mcp_server: MCPServerConfig = Field(default_factory=MCPServerConfig)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    
    # Agent-specific configurations
    research_agent: AgentConfig = Field(
        default_factory=lambda: AgentConfig(
            name="Research Agent",
            temperature=0.3  # Lower temperature for focused research
        )
    )
    analysis_agent: AgentConfig = Field(
        default_factory=lambda: AgentConfig(
            name="Analysis Agent",
            temperature=0.5  # Balanced temperature for analysis
        )
    )
    action_agent: AgentConfig = Field(
        default_factory=lambda: AgentConfig(
            name="Action Agent",
            temperature=0.4  # Strategic temperature for decision-making
        )
    )
    
    # System configurations
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Environment and paths
    data_dir: str = Field(default="./data", description="Data directory path")
    cache_dir: str = Field(default="./.cache", description="Cache directory path")
    log_dir: str = Field(default="./logs", description="Log directory path")
    
    @classmethod
    def from_env(cls) -> 'MultiAgentConfig':
        """Create configuration from environment variables."""
        config_data = {}
        
        # OpenAI configuration
        if os.getenv('OPENAI_API_KEY'):
            config_data['openai'] = {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
                'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
                'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS')) if os.getenv('OPENAI_MAX_TOKENS') else None,
                'timeout': int(os.getenv('OPENAI_TIMEOUT', '60'))
            }
        
        # MCP Server configuration
        config_data['mcp_server'] = {
            'base_url': os.getenv('MCP_SERVER_URL', 'http://localhost:8000'),
            'timeout': int(os.getenv('MCP_TIMEOUT', '30')),
            'max_retries': int(os.getenv('MCP_MAX_RETRIES', '3'))
        }
        
        # Orchestrator configuration
        config_data['orchestrator'] = {
            'max_retries': int(os.getenv('ORCHESTRATOR_MAX_RETRIES', '2')),
            'timeout_per_agent': int(os.getenv('ORCHESTRATOR_TIMEOUT', '300')),
            'parallel_execution': os.getenv('ORCHESTRATOR_PARALLEL', 'false').lower() == 'true',
            'cache_enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
        }
        
        # Logging configuration
        config_data['logging'] = {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'file_logging': os.getenv('FILE_LOGGING', 'true').lower() == 'true',
            'log_file': os.getenv('LOG_FILE', 'orchestrator.log')
        }
        
        # Security configuration
        allowed_domains = os.getenv('ALLOWED_DOMAINS', '')
        blocked_domains = os.getenv('BLOCKED_DOMAINS', '')
        
        config_data['security'] = {
            'rate_limit_requests_per_minute': int(os.getenv('RATE_LIMIT_RPM', '60')),
            'allowed_domains': [d.strip() for d in allowed_domains.split(',') if d.strip()],
            'blocked_domains': [d.strip() for d in blocked_domains.split(',') if d.strip()],
            'max_content_size_mb': int(os.getenv('MAX_CONTENT_SIZE_MB', '10')),
            'enable_content_filtering': os.getenv('CONTENT_FILTERING', 'true').lower() == 'true'
        }
        
        # Database configuration
        config_data['database'] = {
            'db_path': os.getenv('DATABASE_PATH', 'mcp_data.db'),
            'backup_enabled': os.getenv('DB_BACKUP_ENABLED', 'true').lower() == 'true'
        }
        
        # Directories
        config_data.update({
            'data_dir': os.getenv('DATA_DIR', './data'),
            'cache_dir': os.getenv('CACHE_DIR', './.cache'),
            'log_dir': os.getenv('LOG_DIR', './logs')
        })
        
        return cls(**config_data)
    
    @classmethod
    def from_file(cls, config_path: str) -> 'MultiAgentConfig':
        """Load configuration from JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def to_file(self, config_path: str):
        """Save configuration to JSON file."""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a copy without sensitive data for saving
        config_data = self.dict()
        if 'openai' in config_data and 'api_key' in config_data['openai']:
            config_data['openai']['api_key'] = '***HIDDEN***'
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def setup_directories(self):
        """Create necessary directories."""
        directories = [self.data_dir, self.cache_dir, self.log_dir]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate configuration and return any issues."""
        issues = {
            'errors': [],
            'warnings': []
        }
        
        # Check OpenAI API key
        if not self.openai.api_key or self.openai.api_key == '***HIDDEN***':
            issues['errors'].append('OpenAI API key is required')
        
        # Check MCP server URL
        if not self.mcp_server.base_url.startswith(('http://', 'https://')):
            issues['errors'].append('MCP server URL must start with http:// or https://')
        
        # Check directory permissions
        for dir_name, dir_path in [
            ('data', self.data_dir),
            ('cache', self.cache_dir),
            ('log', self.log_dir)
        ]:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                test_file = Path(dir_path) / '.test_write'
                test_file.write_text('test')
                test_file.unlink()
            except Exception as e:
                issues['errors'].append(f'Cannot write to {dir_name} directory ({dir_path}): {e}')
        
        # Check agent configurations
        agents = [self.research_agent, self.analysis_agent, self.action_agent]
        for agent in agents:
            if agent.temperature < 0 or agent.temperature > 2:
                issues['warnings'].append(f'{agent.name} temperature outside recommended range (0-2)')
        
        return issues
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        agent_configs = {
            'research': self.research_agent,
            'analysis': self.analysis_agent,
            'action': self.action_agent
        }
        return agent_configs.get(agent_name.lower())

# Global configuration instance
_config: Optional[MultiAgentConfig] = None

def get_config() -> MultiAgentConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = MultiAgentConfig.from_env()
    return _config

def set_config(config: MultiAgentConfig):
    """Set the global configuration instance."""
    global _config
    _config = config

def load_config_from_file(config_path: str) -> MultiAgentConfig:
    """Load and set configuration from file."""
    config = MultiAgentConfig.from_file(config_path)
    set_config(config)
    return config

def create_default_config_file(config_path: str = "config.json"):
    """Create a default configuration file."""
    default_config = MultiAgentConfig()
    default_config.to_file(config_path)
    return config_path