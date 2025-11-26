"""
Advanced Utility-Based Agent with Enhanced Features
"""
from typing import Dict, List, Tuple, Union, Any, Optional, Callable
from enum import Enum
import math


class DecisionStrategy(Enum):
    MAXIMUM_EXPECTED_UTILITY = "meu"
    MINIMAX = "minimax"
    EXPECTED_VALUE_WITH_KNOWLEDGE = "evk"


class AdvancedUtilityBasedAgent:
    def __init__(self, 
                 actions: Dict[str, List[Dict[str, Union[float, int]]]], 
                 decision_strategy: DecisionStrategy = DecisionStrategy.MAXIMUM_EXPECTED_UTILITY,
                 utility_function: Optional[Callable[[float], float]] = None):
        """
        Initialize the advanced utility-based agent with strategy selection.

        Args:
            actions: Dictionary mapping action names to lists of outcome dictionaries
                    Each outcome dictionary should have 'probability' and 'utility' keys
            decision_strategy: Strategy to use for decision making
            utility_function: Optional custom utility function for transforming utilities
        """
        self.actions = actions
        self.decision_strategy = decision_strategy
        self.utility_function = utility_function
        self.validate_actions()

    def validate_actions(self):
        """Validate that all action outcomes have the required structure."""
        for action_name, outcomes in self.actions.items():
            if not outcomes:
                raise ValueError(f"Action '{action_name}' has no outcomes defined")
                
            total_probability = 0
            for outcome in outcomes:
                if 'probability' not in outcome or 'utility' not in outcome:
                    raise ValueError(f"Action '{action_name}' has invalid outcome structure")
                
                if not 0 <= outcome['probability'] <= 1:
                    raise ValueError(f"Action '{action_name}' has invalid probability: {outcome['probability']}")
                
                total_probability += outcome['probability']
            
            # For most cases, probabilities of outcomes for an action should sum to 1
            # but allow for cases where not all possibilities are listed
            if not abs(total_probability - 1.0) < 0.01 and total_probability > 0:
                print(f"Warning: Action '{action_name}' probabilities sum to {total_probability}, not 1.0")

    def calculate_expected_utility(self, outcomes: List[Dict[str, Union[float, int]]]) -> float:
        """
        Calculate the expected utility for a given action.

        Args:
            outcomes: List of outcome dictionaries with 'probability' and 'utility' keys

        Returns:
            Expected utility value (sum of probability * utility for all outcomes)
        """
        expected_utility = 0
        for outcome in outcomes:
            # Apply custom utility function if provided
            utility = outcome['utility']
            if self.utility_function:
                utility = self.utility_function(utility)
                
            # P(s' | a) * U(s')
            expected_utility += outcome['probability'] * utility
        return expected_utility

    def calculate_minimax_decision(self) -> Tuple[str, float]:
        """
        Decision making using minimax approach (best of worst outcomes).

        Returns:
            Tuple of (best action name, best utility value)
        """
        worst_outcomes = {}
        
        for action, outcomes in self.actions.items():
            # Find the minimum utility outcome for each action (worst case)
            min_utility = min(outcome['utility'] for outcome in outcomes)
            worst_outcomes[action] = min_utility
            
        # Choose the action with the highest minimum utility (best worst-case scenario)
        best_action = max(worst_outcomes, key=worst_outcomes.get)
        best_utility = worst_outcomes[best_action]
        
        return best_action, best_utility

    def calculate_evk_decision(self) -> Tuple[str, float]:
        """
        Decision making using Expected Value of Knowledge approach.

        Returns:
            Tuple of (best action name, best utility value)
        """
        # This approach incorporates the value of information gathering
        # For this implementation, we'll use a simplified EVK that considers risk-adjusted utilities
        evk_results = {}
        
        for action, outcomes in self.actions.items():
            utilities = [outcome['utility'] for outcome in outcomes]
            probabilities = [outcome['probability'] for outcome in outcomes]
            
            # Calculate expected utility
            expected_utility = sum(p * u for p, u in zip(probabilities, utilities))
            
            # Calculate variance as a risk measure
            variance = sum(p * (u - expected_utility)**2 for p, u in zip(probabilities, utilities))
            
            # Risk-adjusted utility = expected utility - risk penalty
            risk_penalty = math.sqrt(variance)  # Using standard deviation as risk measure
            risk_adjusted_utility = expected_utility - risk_penalty
            
            evk_results[action] = risk_adjusted_utility
            
        best_action = max(evk_results, key=evk_results.get)
        best_utility = evk_results[best_action]
        
        return best_action, best_utility

    def decide(self) -> Tuple[str, float, Dict]:
        """
        Decide which action to take based on the selected strategy.

        Returns:
            Tuple of (best action name, best utility value, additional decision info)
        """
        if self.decision_strategy == DecisionStrategy.MAXIMUM_EXPECTED_UTILITY:
            utility_results = {}
            
            # Calculate MEU for each possible action
            for action, outcomes in self.actions.items():
                meu_value = self.calculate_expected_utility(outcomes)
                utility_results[action] = meu_value
            
            if not utility_results:
                return "No valid actions", float('-inf'), {}
            
            # Find the action with the highest expected utility
            best_action = max(utility_results, key=utility_results.get)
            best_meu = utility_results[best_action]
            
            additional_info = {
                'strategy_used': 'Maximum Expected Utility',
                'all_utilities': utility_results,
                'expected_utilities': {action: self.calculate_expected_utility(self.actions[action]) 
                                      for action in self.actions}
            }
            
            return best_action, best_meu, additional_info
            
        elif self.decision_strategy == DecisionStrategy.MINIMAX:
            best_action, best_utility = self.calculate_minimax_decision()
            additional_info = {'strategy_used': 'Minimax'}
            return best_action, best_utility, additional_info
            
        elif self.decision_strategy == DecisionStrategy.EXPECTED_VALUE_WITH_KNOWLEDGE:
            best_action, best_utility = self.calculate_evk_decision()
            additional_info = {'strategy_used': 'Expected Value with Knowledge (Risk-adjusted)'}
            return best_action, best_utility, additional_info
        else:
            raise ValueError(f"Unknown decision strategy: {self.decision_strategy}")

    def analyze_risk_profile(self) -> Dict[str, Any]:
        """
        Analyze the risk profile of each action.

        Returns:
            Dictionary with risk analysis for each action
        """
        risk_analysis = {}
        
        for action, outcomes in self.actions.items():
            utilities = [outcome['utility'] for outcome in outcomes]
            probabilities = [outcome['probability'] for outcome in outcomes]
            
            # Calculate expected utility
            expected_utility = sum(p * u for p, u in zip(probabilities, utilities))
            
            # Calculate variance and standard deviation (risk measures)
            variance = sum(p * (u - expected_utility)**2 for p, u in zip(probabilities, utilities))
            std_dev = math.sqrt(variance)
            
            # Calculate utility range
            utility_range = max(utilities) - min(utilities)
            
            # Coefficient of variation (relative risk)
            coeff_variation = std_dev / abs(expected_utility) if expected_utility != 0 else float('inf')
            
            risk_analysis[action] = {
                'expected_utility': expected_utility,
                'variance': variance,
                'std_deviation': std_dev,
                'utility_range': utility_range,
                'coefficient_variation': coeff_variation,
                'risk_level': self._determine_risk_level(std_dev, expected_utility)
            }
        
        return risk_analysis

    def _determine_risk_level(self, std_dev: float, expected_utility: float) -> str:
        """
        Determine risk level based on standard deviation and expected utility.
        """
        if std_dev == 0:
            return "Risk-free"
        elif expected_utility > 0 and std_dev/expected_utility < 0.5:
            return "Low Risk"
        elif expected_utility > 0 and std_dev/expected_utility < 1.0:
            return "Medium Risk"
        else:
            return "High Risk"


def run_advanced_utility_based_agent_demo():
    """Demo function for the advanced utility-based agent."""
    # Define action outcomes with probabilities and utilities
    ACTION_OUTCOMES = {
        "Conservative Investment": [
            {"probability": 0.8, "utility": 50},   # Moderate gain
            {"probability": 0.2, "utility": 30}    # Lower gain
        ],

        "Moderate Investment": [
            {"probability": 0.6, "utility": 80},   # Good gain
            {"probability": 0.3, "utility": 20},   # Small gain
            {"probability": 0.1, "utility": -40}   # Loss
        ],

        "Aggressive Investment": [
            {"probability": 0.4, "utility": 150},  # High gain
            {"probability": 0.4, "utility": 10},   # Small gain
            {"probability": 0.2, "utility": -100}  # Major loss
        ]
    }

    print("--- Advanced Utility-Based Agent Demo ---\n")

    # Test different decision strategies
    strategies = [
        DecisionStrategy.MAXIMUM_EXPECTED_UTILITY,
        DecisionStrategy.MINIMAX,
        DecisionStrategy.EXPECTED_VALUE_WITH_KNOWLEDGE
    ]
    
    for strategy in strategies:
        print(f"Using strategy: {strategy.value}")
        print("-" * 40)
        
        agent = AdvancedUtilityBasedAgent(ACTION_OUTCOMES, decision_strategy=strategy)
        best_action, best_utility, additional_info = agent.decide()
        
        print(f"Best action: {best_action}")
        print(f"Best utility: {best_utility}")
        print(f"Strategy used: {additional_info.get('strategy_used', 'Unknown')}")
        
        if strategy == DecisionStrategy.MAXIMUM_EXPECTED_UTILITY:
            print("\nAction evaluation:")
            for action, outcomes in ACTION_OUTCOMES.items():
                meu_value = agent.calculate_expected_utility(outcomes)
                print(f"  {action}: {meu_value}")
        
        print()

    # Risk analysis
    print("Risk Analysis:")
    print("-" * 40)
    risk_agent = AdvancedUtilityBasedAgent(ACTION_OUTCOMES)
    risk_analysis = risk_agent.analyze_risk_profile()
    
    for action, analysis in risk_analysis.items():
        print(f"  {action}:")
        print(f"    - Expected utility: {analysis['expected_utility']}")
        print(f"    - Standard deviation (risk): {analysis['std_deviation']:.2f}")
        print(f"    - Risk level: {analysis['risk_level']}")
        print()

    # Comparison
    print("Strategy Comparison:")
    print("-" * 40)
    for strategy in strategies:
        agent = AdvancedUtilityBasedAgent(ACTION_OUTCOMES, decision_strategy=strategy)
        best_action, best_utility, _ = agent.decide()
        print(f"  {strategy.value}: {best_action} (Utility: {best_utility})")


if __name__ == "__main__":
    run_advanced_utility_based_agent_demo()