"""
Hybrid AI Agent: Combines Goal-Based and Utility-Based Approaches
"""
from typing import Dict, List, Tuple, Optional, Union, Any
from advanced_goal_based_agent import AdvancedGoalBasedAgent, PathfindingAlgorithm
from advanced_utility_based_agent import AdvancedUtilityBasedAgent, DecisionStrategy


class HybridAgent:
    """
    A hybrid agent that combines goal-based and utility-based decision making.
    
    This agent uses goal-based reasoning to find possible paths to the goal,
    then uses utility-based reasoning to evaluate and select the best path
    based on additional utility factors beyond just path cost.
    """
    
    def __init__(self, 
                 routes: Dict[str, List[Tuple[str, int]]],
                 start: str,
                 goal: str,
                 path_evaluation_factors: Optional[Dict[str, float]] = None):
        """
        Initialize the hybrid agent.
        
        Args:
            routes: Dictionary mapping nodes to (destination, cost) tuples
            start: Starting node
            goal: Goal node
            path_evaluation_factors: Additional factors to consider when evaluating paths
        """
        self.routes = routes
        self.start = start
        self.goal = goal
        self.path_evaluation_factors = path_evaluation_factors or {}
        
        # Cache of best paths found so far (mainly for debugging/inspection)
        self.best_paths: List[Tuple[List[str], float]] = []
        
    def find_multiple_paths(self, num_paths: int = 3) -> List[Tuple[List[str], float]]:
        """Find up to ``num_paths`` reasonably good alternative paths.

        This now delegates to :class:`AdvancedGoalBasedAgent`'s ``find_all_paths``
        implementation, which already implements a k-shortest-paths style search.
        """
        primary_agent = AdvancedGoalBasedAgent(self.routes, self.start, self.goal)
        all_paths = primary_agent.find_all_paths()

        # Trim to the requested number of paths
        trimmed_paths = all_paths[: max(num_paths, 0)] if all_paths else []
        self.best_paths = trimmed_paths
        return trimmed_paths
    
    def evaluate_paths_with_utility(self, paths: List[Tuple[List[str], float]]) -> Dict:
        """
        Evaluate multiple paths using utility-based reasoning.
        
        Args:
            paths: List of (path, cost) tuples
            
        Returns:
            Dictionary with evaluation results
        """
        # Create action outcomes for each path
        action_outcomes = {}
        
        for i, (path, base_cost) in enumerate(paths):
            path_name = f"Path_{i+1}_({' -> '.join(path)})"
            
            # Define potential outcomes for this path
            # Success and complication probabilities depend on path length: longer
            # paths have slightly higher chance of complications.
            path_length = max(len(path) - 1, 1)
            complication_prob = min(0.1 + 0.02 * (path_length - 1), 0.4)
            success_prob = max(1.0 - complication_prob, 0.0)

            # Base utility is negative cost (we want lower-cost paths) scaled a bit
            base_utility = -float(base_cost)

            outcomes = [
                {
                    "probability": success_prob,
                    "utility": base_utility,
                },
                {
                    "probability": complication_prob,
                    "utility": base_utility * 1.5,  # more negative when complications occur
                },
            ]
            
            # Add path-specific factors if available (length penalties, node penalties, etc.)
            if self.path_evaluation_factors:
                # Apply additional evaluation factors to the success-case utility
                adjusted_utility = self._apply_evaluation_factors(outcomes[0]["utility"], path)
                outcomes[0]["utility"] = adjusted_utility
            
            action_outcomes[path_name] = outcomes
        
        # Use utility-based agent to decide
        utility_agent = AdvancedUtilityBasedAgent(action_outcomes)
        best_path, best_utility, additional_info = utility_agent.decide()
        
        return {
            'best_path': best_path,
            'best_utility': best_utility,
            'all_paths_evaluation': action_outcomes,
            'decision_info': additional_info
        }
    
    def _apply_evaluation_factors(self, base_utility: float, path: List[str]) -> float:
        """
        Apply additional evaluation factors to the base utility of a path.
        """
        adjusted_utility = base_utility
        
        # Example: adjust for path length
        if 'path_length_factor' in self.path_evaluation_factors:
            length_penalty = len(path) * self.path_evaluation_factors['path_length_factor']
            adjusted_utility += length_penalty
        
        # Example: adjust for specific nodes (e.g., avoid dangerous nodes)
        if 'node_penalties' in self.path_evaluation_factors:
            for node in path:
                if node in self.path_evaluation_factors['node_penalties']:
                    adjusted_utility += self.path_evaluation_factors['node_penalties'][node]
        
        return adjusted_utility
    
    def make_decision(self) -> Dict[str, Any]:
        """
        Make a decision using the hybrid approach.
        
        Returns:
            Dictionary with decision results
        """
        # Step 1: Use goal-based agent to find potential paths
        all_paths = self.find_multiple_paths(num_paths=3)
        
        if not all_paths:
            return {
                'success': False,
                'message': f'No path found from {self.start} to {self.goal}',
                'best_path': None,
                'best_utility': float('-inf')
            }
        
        # Step 2: Use utility-based agent to evaluate and select best path
        evaluation = self.evaluate_paths_with_utility(all_paths)
        
        # Step 3: Format and return results
        best_path_name = evaluation['best_path']
        
        # Extract the actual path from the path name
        # Format is like "Path_1_(A -> B -> C)" - extract the part in parentheses
        import re
        match = re.search(r'\((.*)\)', best_path_name)
        if match:
            path_str = match.group(1)
            path_nodes = path_str.split(" -> ")
        else:
            # If regex fails, try to parse differently
            path_nodes = best_path_name.split(" -> ")
        
        return {
            'success': True,
            'best_path': evaluation['best_path'],
            'path_as_list': path_nodes,
            'best_utility': evaluation['best_utility'],
            'all_evaluated_paths': evaluation['all_paths_evaluation'],
            'decision_info': evaluation['decision_info'],
            'num_paths_considered': len(all_paths)
        }


class LearningPathAdvisorWithHybridAgent:
    """
    Enhanced Learning Path Advisor using the Hybrid Agent approach
    """
    def __init__(self):
        """
        Initialize the enhanced learning path advisor
        """
        # Course database with prerequisites and dependencies - Using the same as enhanced_learning_path_advisor
        from enhanced_learning_path_advisor import EnhancedLearningPathAdvisor
        advisor = EnhancedLearningPathAdvisor()
        
        # Get course data from the existing enhanced advisor
        self.course_prerequisites = advisor.course_prerequisites
        self.course_attributes = advisor.course_attributes
        
        # Create graph representation for pathfinding
        self.course_graph = self._build_course_graph()

    def _build_course_graph(self) -> Dict[str, List[Tuple[str, int]]]:
        """
        Build a graph representation of courses for pathfinding
        """
        graph = {course: [] for course in self.course_prerequisites}

        # Add edges for courses that have prerequisites
        for course, prereqs in self.course_prerequisites.items():
            for prereq in prereqs:
                if prereq in graph:
                    # Using difficulty as the edge weight
                    cost = self.course_attributes[course]['difficulty']
                    graph[prereq].append((course, cost))

        return graph

    def find_optimal_learning_path(self, start_courses: List[str], goal_course: str) -> Dict:
        """
        Find the optimal learning path using the hybrid agent approach
        """
        # Create a temporary graph for this specific query
        temp_graph = {**self.course_graph}
        
        # Add virtual start node to connect all start courses
        temp_graph['virtual_start'] = []
        for start_course in start_courses:
            if start_course in self.course_graph:
                # Cost of 0 to start from completed course
                temp_graph['virtual_start'].append((start_course, 0))
        
        # Add the virtual start to prerequisites if needed
        if 'virtual_start' not in self.course_prerequisites:
            self.course_prerequisites['virtual_start'] = []
            self.course_attributes['virtual_start'] = {'difficulty': 0, 'time_hours': 0, 'utility': 0}

        # Use hybrid agent for decision making
        hybrid_agent = HybridAgent(
            routes=temp_graph,
            start='virtual_start', 
            goal=goal_course,
            path_evaluation_factors={
                'path_length_factor': -0.5,  # Prefer shorter paths
                'node_penalties': {course: -attr['utility']*0.1 
                                  for course, attr in self.course_attributes.items()}
            }
        )
        
        decision = hybrid_agent.make_decision()
        
        # Format the result
        if decision['success']:
            # Remove virtual_start from the path
            final_path = [node for node in decision['path_as_list'] if node != 'virtual_start']
            path_str = " -> ".join(final_path)
        else:
            path_str = None
            final_path = []
        
        return {
            'success': decision['success'],
            'path': path_str,
            'path_list': final_path,
            'utility': decision.get('best_utility', float('-inf')),
            'start_courses': start_courses,
            'goal_course': goal_course,
            'all_considered_paths': decision.get('all_evaluated_paths', {}),
            'decision_info': decision.get('decision_info', {})
        }


def run_hybrid_agent_demo():
    """Demo function for the hybrid agent."""
    print("--- Hybrid AI Agent Demo ---")
    print("Combining Goal-Based and Utility-Based Decision Making\n")
    
    # Define a sample graph
    MAP_ROUTES = {
        'A': [('B', 3), ('C', 5), ('E', 10)],
        'B': [('D', 4), ('E', 2)],
        'C': [('D', 2)],
        'D': [('F', 3)],
        'E': [('F', 1)],
        'F': []  # F is the goal
    }

    START_NODE = 'A'
    GOAL_NODE = 'F'

    print(f"Goal: Reach {GOAL_NODE}")
    print(f"Starting Point: {START_NODE}\n")

    # Create hybrid agent
    hybrid_agent = HybridAgent(
        routes=MAP_ROUTES,
        start=START_NODE, 
        goal=GOAL_NODE,
        path_evaluation_factors={
            'path_length_factor': -0.5,  # Prefer shorter paths
            'node_penalties': {'E': -2, 'B': -1}  # Penalize certain nodes
        }
    )
    
    decision = hybrid_agent.make_decision()
    
    print("Hybrid Agent Decision Results:")
    print(f"  - Success: {decision['success']}")
    print(f"  - Best Path: {decision['best_path']}")
    print(f"  - Best Utility: {decision['best_utility']}")
    print(f"  - Number of paths considered: {decision['num_paths_considered']}")
    
    if decision['success']:
        print(f"  - Path as list: {decision['path_as_list']}")
    
    print("\n" + "="*50)
    
    # Demo the enhanced learning path advisor
    print("\n--- Enhanced Learning Path Advisor with Hybrid Agent ---")
    advisor = LearningPathAdvisorWithHybridAgent()
    
    result = advisor.find_optimal_learning_path(['Python Basics'], 'Data Structures')
    print(f"Learning Path from Python Basics to Data Structures:")
    print(f"  - Success: {result['success']}")
    print(f"  - Path: {result['path']}")
    print(f"  - Utility: {result['utility']}")


if __name__ == "__main__":
    run_hybrid_agent_demo()