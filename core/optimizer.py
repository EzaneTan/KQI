import yaml
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KQI Agent Optimizer")

class AgentOptimizer:
    """
    A class to analyze and optimize KQI agents based on their performance.
    """

    def __init__(self, config_path: str, performance_data_path: Optional[str] = None):
        """
        Initialize the AgentOptimizer with the path to the agent's configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.
            performance_data_path (Optional[str]): Path to the performance data file.
        """
        self.config_path = config_path
        self.config: Dict = self._load_config()
        self.performance_data_path = performance_data_path or f"./reports/{self.config['agent']['name']}_performance.yaml"
        self.performance_data: Dict = self._load_performance_data()

    def _load_config(self) -> Dict:
        """
        Load the agent configuration from the YAML file.

        Returns:
            Dict: The loaded configuration.
        """
        try:
            with open(self.config_path, "r") as file:
                config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from: {self.config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise

    def _load_performance_data(self) -> Dict:
        """
        Load the agent's performance data from the YAML file.

        Returns:
            Dict: The loaded performance data.
        """
        try:
            with open(self.performance_data_path, "r") as file:
                performance_data = yaml.safe_load(file)
                logger.info(f"Performance data loaded from: {self.performance_data_path}")
                return performance_data or {}
        except FileNotFoundError:
            logger.warning(f"Performance data file not found: {self.performance_data_path}")
            return {}

    def generate_report(self) -> Dict:
        """
        Generate a performance report for the agent.

        Returns:
            Dict: A dictionary containing the performance report.
        """
        report = {
            "agent_name": self.config["agent"]["name"],
            "strategy": self.config["agent"]["strategy"],
            "risk_level": self.config["agent"]["risk_level"],
            "protocols": self.config["agent"]["protocols"],
            "performance_metrics": self.performance_data.get("metrics", {}),
            "suggestions": self._generate_optimization_suggestions(),
            "timestamp": datetime.now().isoformat(),
        }

        logger.info("Performance report generated.")
        return report

    def _generate_optimization_suggestions(self) -> List[str]:
        """
        Generate optimization suggestions based on performance data.

        Returns:
            List[str]: A list of optimization suggestions.
        """
        suggestions = []
        metrics = self.performance_data.get("metrics", {})

        # Example optimization logic
        if metrics.get("profitability", 0) < 0:
            suggestions.append("Consider adjusting the strategy to reduce losses.")
        if metrics.get("trade_execution_time", 0) > 1.0:  # Example threshold
            suggestions.append("Optimize trade execution to reduce latency.")
        if len(self.config["agent"]["protocols"]) < 2:
            suggestions.append("Add more protocols to diversify trading opportunities.")

        return suggestions

    def save_report(self, report: Dict, report_path: Optional[str] = None) -> str:
        """
        Save the performance report to a YAML file.

        Args:
            report (Dict): The performance report to save.
            report_path (Optional[str]): The path to save the report file.
                                      If not provided, defaults to `./reports/{agent_name}_report.yaml`.

        Returns:
            str: The path to the saved report file.
        """
        if report_path is None:
            report_path = f"./reports/{self.config['agent']['name']}_report.yaml"

        # Ensure the reports directory exists
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w") as file:
            yaml.dump(report, file)

        logger.info(f"Performance report saved to: {report_path}")
        return report_path

    def optimize(self, new_risk_level: Optional[float] = None, new_strategy: Optional[str] = None) -> None:
        """
        Optimize the agent's configuration based on performance data.

        Args:
            new_risk_level (Optional[float]): The new risk level to set.
            new_strategy (Optional[str]): The new strategy to set.
        """
        if new_risk_level is not None:
            if 0.0 <= new_risk_level <= 1.0:
                self.config["agent"]["risk_level"] = new_risk_level
                logger.info(f"Risk level updated to: {new_risk_level}")
            else:
                raise ValueError("Risk level must be between 0.0 and 1.0")

        if new_strategy is not None:
            self.config["agent"]["strategy"] = new_strategy
            logger.info(f"Strategy updated to: {new_strategy}")

        # Save the updated configuration
        self.save_config()

    def save_config(self) -> str:
        """
        Save the updated agent configuration to the YAML file.

        Returns:
            str: The path to the saved configuration file.
        """
        with open(self.config_path, "w") as file:
            yaml.dump(self.config, file)

        logger.info(f"Updated configuration saved to: {self.config_path}")
        return self.config_path


# Example Usage
if __name__ == "__main__":
    # Path to the agent configuration file
    config_path = "./config/my_agent.yaml"

    # Initialize the optimizer
    optimizer = AgentOptimizer(config_path)

    # Generate and save a performance report
    report = optimizer.generate_report()
    optimizer.save_report(report)

    # Optimize the agent
    optimizer.optimize(new_risk_level=0.6, new_strategy="market_making")

    # Save the updated configuration
    optimizer.save_config()