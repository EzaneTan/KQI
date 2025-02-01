import yaml
import logging
from typing import Dict, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KQI Agent Builder")

class AgentBuilder:
    """
    A builder class for creating and configuring KQI agents.
    """

    def __init__(self, agent_name: str):
        """
        Initialize the AgentBuilder with a name for the agent.

        Args:
            agent_name (str): The name of the agent.
        """
        self.agent_name = agent_name
        self.config: Dict = {
            "agent": {
                "name": agent_name,
                "strategy": None,
                "risk_level": 0.5,  # Default risk level
                "protocols": [],
            },
            "api": {
                "key": None,
            },
        }

    def set_strategy(self, strategy: str) -> "AgentBuilder":
        """
        Set the trading strategy for the agent.

        Args:
            strategy (str): The name of the strategy (e.g., "arbitrage", "market_making").

        Returns:
            AgentBuilder: The builder instance for method chaining.
        """
        self.config["agent"]["strategy"] = strategy
        logger.info(f"Strategy set to: {strategy}")
        return self

    def set_risk_level(self, risk_level: float) -> "AgentBuilder":
        """
        Set the risk level for the agent (0.0 to 1.0).

        Args:
            risk_level (float): The risk level (0.0 = low risk, 1.0 = high risk).

        Returns:
            AgentBuilder: The builder instance for method chaining.
        """
        if 0.0 <= risk_level <= 1.0:
            self.config["agent"]["risk_level"] = risk_level
            logger.info(f"Risk level set to: {risk_level}")
        else:
            raise ValueError("Risk level must be between 0.0 and 1.0")
        return self

    def add_protocol(self, protocol: str) -> "AgentBuilder":
        """
        Add a DeFi protocol for the agent to interact with.

        Args:
            protocol (str): The name of the protocol (e.g., "uniswap", "sushiswap").

        Returns:
            AgentBuilder: The builder instance for method chaining.
        """
        self.config["agent"]["protocols"].append(protocol)
        logger.info(f"Added protocol: {protocol}")
        return self

    def set_api_key(self, api_key: str) -> "AgentBuilder":
        """
        Set the API key for the KQI platform.

        Args:
            api_key (str): The API key obtained from the KQI dashboard.

        Returns:
            AgentBuilder: The builder instance for method chaining.
        """
        self.config["api"]["key"] = api_key
        logger.info("API key set successfully")
        return self

    def save_config(self, file_path: Optional[str] = None) -> str:
        """
        Save the agent configuration to a YAML file.

        Args:
            file_path (Optional[str]): The path to save the configuration file.
                                      If not provided, defaults to `./config/{agent_name}.yaml`.

        Returns:
            str: The path to the saved configuration file.
        """
        if file_path is None:
            file_path = f"./config/{self.agent_name}.yaml"
        
        # Ensure the config directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(self.config, file)
        
        logger.info(f"Configuration saved to: {file_path}")
        return file_path

    def deploy(self) -> bool:
        """
        Deploy the agent to the KQI platform.

        Returns:
            bool: True if deployment is successful, False otherwise.
        """
        if not self.config["agent"]["strategy"]:
            raise ValueError("No strategy defined. Use `set_strategy()` to define one.")
        if not self.config["api"]["key"]:
            raise ValueError("No API key provided. Use `set_api_key()` to set one.")

        # Simulate deployment (replace with actual deployment logic)
        logger.info(f"Deploying agent '{self.agent_name}' with strategy '{self.config['agent']['strategy']}'...")
        logger.info("Agent deployed successfully!")
        return True


# Example Usage
if __name__ == "__main__":
    # Create and configure an agent
    builder = (
        AgentBuilder("MyFirstAgent")
        .set_strategy("arbitrage")
        .set_risk_level(0.7)
        .add_protocol("uniswap")
        .add_protocol("sushiswap")
        .set_api_key("your_api_key_here")
    )

    # Save the configuration
    config_path = builder.save_config()

    # Deploy the agent
    builder.deploy()