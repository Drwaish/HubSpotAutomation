"""
Enhanced CRM Agent Orchestrator

This module provides a comprehensive CRM assistant that integrates with HubSpot and Gmail
through various agent tools. It uses LangChain's agent framework with Groq LLM for
intelligent task execution based on user requests.

Key Features:
- Contact management (create, update)
- Deal management (create, update)
- Email sending capabilities
- Intelligent tool selection based on user input
- Comprehensive error handling and logging
- Configurable LLM settings
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    from agent.agent_tools import AgentTools
    from langchain_groq import ChatGroq
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import AgentAction, AgentFinish
except ImportError as e:
    print(f"Required dependencies not installed: {e}")
    print("Please install: pip install langchain langchain-groq")
    sys.exit(1)


@dataclass
class AgentConfig:
    """Configuration settings for the CRM Agent"""
    model_name: str = "mixtral-8x7b-32768"
    temperature: float = 0.1
    max_tokens: int = 1024
    max_iterations: int = 5
    verbose: bool = True
    return_intermediate_steps: bool = True

logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
logger = logging.getLogger(__name__)
class AgentOrchestrator:
    """
    A comprehensive CRM assistant that orchestrates various tools for HubSpot and Gmail operations.
    
    This class manages the integration between language models and CRM tools, providing
    intelligent assistance for contact management, deal tracking, and email operations.
    
    Attributes:
        llm: The language model instance (ChatGroq)
        agent_tools: Instance of AgentTools containing CRM functionality
        tools: List of available tools for the agent
        agent_executor: The main agent executor for handling requests
        config: Configuration settings for the agent
    """
    
    def __init__(self, groq_api_key: Optional[str] = None, agent_tools: Optional[AgentTools] = None, 
                 config: Optional[AgentConfig] = None):
        """
        Initialize the CRM Agent Orchestrator.
        
        Args:
            groq_api_key: API key for Groq LLM (if not provided, will use environment variable)
            agent_tools: Instance of AgentTools (if not provided, will create new instance)
            config: Configuration settings (if not provided, will use defaults)
        
        Raises:
            ValueError: If Groq API key is not provided or found in environment
            RuntimeError: If agent tools cannot be initialized
        """
        self.config = config or AgentConfig()
        self._setup_logging()
        
        # Initialize LLM
        self.llm = self._initialize_llm(groq_api_key)
        
        # Initialize agent tools
        self.agent_tools = agent_tools or self._initialize_agent_tools()
        
        # Setup tools and create agent
        self.tools = self._setup_tools()
        self.agent_executor = self._create_agent_executor()
        
        logger.info("CRM Agent Orchestrator initialized successfully")
    
    
    
    def _initialize_llm(self, groq_api_key: Optional[str] = None) -> ChatGroq:
        """
        Initialize the Groq LLM with proper configuration.
        
        Args:
            groq_api_key: API key for Groq (optional if set in environment)
            
        Returns:
            ChatGroq: Configured language model instance
            
        Raises:
            ValueError: If API key is not provided
        """
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "Groq API key is required. Provide it as parameter or set GROQ_API_KEY environment variable."
            )
        
        try:
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            logger.info(f"LLM initialized with model: {self.config.model_name}")
            return llm
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise RuntimeError(f"LLM initialization failed: {e}")
    
    def _initialize_agent_tools(self) -> AgentTools:
        """
        Initialize agent tools with error handling.
        
        Returns:
            AgentTools: Instance of agent tools
            
        Raises:
            RuntimeError: If agent tools cannot be initialized
        """
        try:
            tools = AgentTools()
            logger.info("Agent tools initialized successfully")
            return tools
        except Exception as e:
            logger.error(f"Failed to initialize agent tools: {e}")
            raise RuntimeError(f"Agent tools initialization failed: {e}")
    
    def _setup_tools(self) -> List:
        """
        Setup and validate all available tools.
        
        Returns:
            List: List of available tools for the agent
        """
        tools = []
        tool_methods = [
            ('update_contacts', 'Update existing contacts in HubSpot'),
            ('create_contact', 'Create new contacts in HubSpot'),
            ('create_deal', 'Create new deals in HubSpot'),
            ('update_deal', 'Update existing deals in HubSpot'),
            ('send_email', 'Send emails via Gmail integration')
        ]
        
        for tool_name, description in tool_methods:
            try:
                tool = getattr(self.agent_tools, tool_name)
                tools.append(tool)
                logger.debug(f"Added tool: {tool_name} - {description}")
            except AttributeError:
                logger.warning(f"Tool {tool_name} not available in agent_tools")
        
        if not tools:
            raise RuntimeError("No tools available for the agent")
        
        logger.info(f"Loaded {len(tools)} tools successfully")
        return tools
    
    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create the main agent executor with comprehensive prompt.
        
        Returns:
            AgentExecutor: Configured agent executor
        """
        # Create a comprehensive prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("user", "{input}"),
            ("assistant", "{agent_scratchpad}")
        ])
        
        # Create the tool-calling agent
        agent = create_tool_calling_agent(self.llm, self.tools, prompt_template)
        
        # Create and return the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.config.verbose,
            return_intermediate_steps=self.config.return_intermediate_steps,
            max_iterations=self.config.max_iterations,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    def _get_system_prompt(self) -> str:
        """
        Get the comprehensive system prompt for the CRM assistant.
        
        Returns:
            str: Detailed system prompt
        """
        return """
        You are an intelligent CRM assistant specializing in HubSpot and Gmail operations.
        Your primary goal is to help users efficiently manage their customer relationships.
        
        AVAILABLE CAPABILITIES:
        1. Contact Management:
           - Create new contacts with complete information
           - Update existing contact details
           - Search and retrieve contact information
        
        2. Deal Management:
           - Create new deals with proper pipeline assignment
           - Update deal stages, values, and properties
           - Track deal progression and outcomes
        
        3. Email Operations:
           - Send personalized emails via Gmail
           - Compose professional communications
           - Handle email templates and formatting
        
        OPERATION GUIDELINES:
        - Always confirm important actions before execution
        - Ask for clarification if user requests are ambiguous
        - Provide clear feedback on completed actions
        - Handle errors gracefully and suggest alternatives
        - Maintain professional communication standards
        
        RESPONSE FORMAT:
        - Be concise but comprehensive
        - Use bullet points for multiple items
        - Include relevant details about completed actions
        - Suggest next steps when appropriate
        
        Remember: You have access to tools that can perform real operations in HubSpot and Gmail.
        Always use the most appropriate tool for each task and validate inputs before proceeding.
        """
    
    def run(self, user_input: str) ->str:
        """
        Execute user request through the agent system.
        
        Args:
            user_input: User's request or query
            
        Returns:
            Dict[str, Any]: Response containing output and intermediate steps
            
        Raises:
            ValueError: If user input is empty or invalid
            RuntimeError: If agent execution fails
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
        
        logger.info(f"Processing user request: {user_input[:100]}...")
        
        try:
            # Execute the agent
            result = self.agent_executor.invoke({
                "input": user_input.strip()
            })
            
            logger.info("Request processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise RuntimeError(f"Failed to process request: {e}")



def main():
    """
    Main function to run the CRM Assistant.
    """
    try:
        # Initialize the agent orchestrator
        agent_tools = AgentTools()
        config = AgentConfig(verbose=True, temperature=0.1)
        
        orchestrator = AgentOrchestrator(
            agent_tools=agent_tools,
            config=config
        )
        
        orchestrator.run(user_input = "Hi")
        
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()