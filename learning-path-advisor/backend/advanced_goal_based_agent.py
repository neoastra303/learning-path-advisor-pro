"""
Advanced Goal-Based Agent with Enhanced Features
"""
import heapq
from typing import Dict, List, Tuple, Optional, Callable, Any
from enum import Enum


class PathfindingAlgorithm(Enum):
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"
    BFS = "bfs"


class AdvancedGoalBasedAgent:
    def __init__(self, 
                 routes: Dict[str, List[Tuple[str, float]]], 
                 start: str, 
                 goal: str,
                 heuristic: Optional[Callable[[str, str], float]] = None,
                 algorithm: PathfindingAlgorithm = PathfindingAlgorithm.DIJKSTRA):
        """
        Initialize the advanced goal-based agent with optional heuristic and algorithm selection.

        Args:
            routes: Dictionary mapping nodes to (destination, cost) tuples
            start: Starting node
            goal: Target node
            heuristic: Optional heuristic function for A* algorithm
            algorithm: Pathfinding algorithm to use
        """
        self.routes = routes
        self.start = start
        self.goal = goal
        self.heuristic = heuristic
        self.algorithm = algorithm
        self.validate_graph()

    def validate_graph(self):
        """Validate that the graph structure is correct."""
        if self.start not in self.routes:
            raise ValueError(f"Start node '{self.start}' not in routes")
        if self.goal not in self.routes:
            raise ValueError(f"Goal node '{self.goal}' not in routes")

        # Check that all routes have valid destinations
        for node, connections in self.routes.items():
            for dest, cost in connections:
                if dest not in self.routes:
                    print(f"Warning: Route from {node} to {dest} points to non-existent node")

    def dijkstra_pathfinding(self) -> Tuple[Optional[List[str]], float]:
        """
        Find the shortest path using Dijkstra's algorithm.

        Returns:
            Tuple of (path as list of nodes, total cost) or (None, infinity) if no path exists
        """
        # Initialize distances and previous nodes
        distances = {node: float('inf') for node in self.routes}
        distances[self.start] = 0
        previous = {node: None for node in self.routes}
        unvisited = [(0, self.start)]
        visited = set()

        while unvisited:
            current_distance, current_node = heapq.heappop(unvisited)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == self.goal:
                break

            for neighbor, weight in self.routes[current_node]:
                if neighbor not in visited:
                    new_distance = current_distance + weight

                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_node
                        heapq.heappush(unvisited, (new_distance, neighbor))

        # Reconstruct path
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if path[0] != self.start:
            return None, float('inf')  # No path found

        return path, distances[self.goal]

    def astar_pathfinding(self) -> Tuple[Optional[List[str]], float]:
        """
        Find the shortest path using A* algorithm with heuristic.

        Returns:
            Tuple of (path as list of nodes, total cost) or (None, infinity) if no path exists
        """
        if self.heuristic is None:
            raise ValueError("Heuristic function is required for A* algorithm")

        # Initialize distances and previous nodes
        g_score = {node: float('inf') for node in self.routes}
        g_score[self.start] = 0
        f_score = {node: float('inf') for node in self.routes}
        f_score[self.start] = self.heuristic(self.start, self.goal)
        
        previous = {node: None for node in self.routes}
        open_set = [(f_score[self.start], self.start)]
        closed_set = set()

        while open_set:
            _, current_node = heapq.heappop(open_set)

            if current_node in closed_set:
                continue

            closed_set.add(current_node)

            if current_node == self.goal:
                break

            for neighbor, weight in self.routes[current_node]:
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current_node] + weight

                if tentative_g_score < g_score[neighbor]:
                    previous[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Reconstruct path
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if not path or path[0] != self.start:
            return None, float('inf')  # No path found

        return path, g_score[self.goal]

    def bfs_pathfinding(self) -> Tuple[Optional[List[str]], float]:
        """Find a path using breadth-first search (treating all edges as unit cost).

        This is useful when edge weights are uniform or when we care primarily
        about the number of steps rather than the weighted cost.
        """
        from collections import deque

        queue = deque([self.start])
        previous = {node: None for node in self.routes}
        visited = {node: False for node in self.routes}
        visited[self.start] = True

        while queue:
            current = queue.popleft()
            if current == self.goal:
                break

            for neighbor, _ in self.routes.get(current, []):
                if not visited.get(neighbor, False):
                    visited[neighbor] = True
                    previous[neighbor] = current
                    queue.append(neighbor)

        # Reconstruct path
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if not path or path[0] != self.start:
            return None, float('inf')  # No path found

        # Cost is simply the number of edges along the path
        return path, float(max(len(path) - 1, 0))

    def find_all_paths(self, max_cost: float = float('inf')) -> List[Tuple[List[str], float]]:
        """
        Find multiple alternative paths from start to goal using a modified Yen's algorithm approach.

        Args:
            max_cost: Maximum cost threshold for paths to be considered

        Returns:
            List of (path, cost) tuples
        """
        # First, find the shortest path using the primary algorithm
        shortest_path, shortest_cost = self.dijkstra_pathfinding()
        
        if not shortest_path or shortest_cost > max_cost:
            return []
        
        all_paths = [(shortest_path, shortest_cost)]
        
        # Now find k-shortest paths by removing each edge of the previous path
        # and finding the next shortest path in the modified graph
        potential_candidates = []
        
        # For each edge in the shortest path, remove it and find an alternative
        for i in range(len(shortest_path) - 1):
            # Create a modified graph by removing the current edge
            modified_routes = {k: [] for k in self.routes.keys()}
            for node, edges in self.routes.items():
                for dest, cost in edges:
                    # Skip the edge we're removing
                    if not (node == shortest_path[i] and dest == shortest_path[i+1]):
                        modified_routes[node].append((dest, cost))
            
            # Create a temporary agent with the modified graph
            temp_agent = AdvancedGoalBasedAgent(
                modified_routes, 
                self.start, 
                self.goal,
                algorithm=PathfindingAlgorithm.DIJKSTRA
            )
            
            alt_path, alt_cost = temp_agent.dijkstra_pathfinding()
            if alt_path and alt_cost <= max_cost:
                # Ensure this path is not already in our results
                if alt_path not in [p for p, _ in all_paths]:
                    potential_candidates.append((alt_path, alt_cost))
        
        # Sort candidates by cost and add to results
        potential_candidates.sort(key=lambda x: x[1])  # Sort by cost ascending
        for path, cost in potential_candidates:
            if path not in [p for p, _ in all_paths]:
                all_paths.append((path, cost))
        
        # Now also try to find paths by removing nodes instead of edges
        # This can help find more diverse paths
        for node in shortest_path[1:-1]:  # Don't remove start or goal nodes
            modified_routes = {k: [(dest, cost) for dest, cost in v if dest != node] 
                              for k, v in self.routes.items()}
            # Remove the node completely from the graph
            if node in modified_routes:
                modified_routes[node] = []
            
            temp_agent = AdvancedGoalBasedAgent(
                modified_routes, 
                self.start, 
                self.goal,
                algorithm=PathfindingAlgorithm.DIJKSTRA
            )
            
            alt_path, alt_cost = temp_agent.dijkstra_pathfinding()
            if alt_path and alt_cost <= max_cost:
                if alt_path not in [p for p, _ in all_paths]:
                    all_paths.append((alt_path, alt_cost))
        
        # Return unique paths sorted by cost
        unique_paths = []
        seen_paths = set()
        for path, cost in all_paths:
            path_str = " -> ".join(path)
            if path_str not in seen_paths:
                unique_paths.append((path, cost))
                seen_paths.add(path_str)
        
        return sorted(unique_paths, key=lambda x: x[1])

    def plan(self) -> Tuple[Optional[str], float]:
        """
        Plan the optimal path from start to goal using selected algorithm.

        Returns:
            Tuple of (path description, total cost)
        """
        if self.algorithm == PathfindingAlgorithm.DIJKSTRA:
            path, cost = self.dijkstra_pathfinding()
        elif self.algorithm == PathfindingAlgorithm.ASTAR:
            path, cost = self.astar_pathfinding()
        elif self.algorithm == PathfindingAlgorithm.BFS:
            path, cost = self.bfs_pathfinding()
        else:
            # Fallback to Dijkstra for unknown algorithms
            path, cost = self.dijkstra_pathfinding()
        
        if path is None:
            return None, float('inf')

        return " -> ".join(path), cost

    def get_path_details(self) -> Dict[str, Any]:
        """
        Get comprehensive details about the path and alternatives.

        Returns:
            Dictionary with path information
        """
        best_path_str, best_cost = self.plan()

        # If no path exists, return a structured failure response
        if best_path_str is None or best_cost == float('inf'):
            return {
                "best_path": [],
                "best_cost": float('inf'),
                "all_alternative_paths": [],
                "start_node": self.start,
                "goal_node": self.goal,
                "algorithm_used": self.algorithm.value,
                "success": False,
                "message": f"No path found from {self.start} to {self.goal}"
            }

        best_path = best_path_str.split(" -> ") if best_path_str else []
        
        all_paths = self.find_all_paths(max_cost=best_cost * 2)  # Find paths up to 2x the best cost
        
        return {
            "best_path": best_path,
            "best_cost": best_cost,
            "all_alternative_paths": all_paths,
            "start_node": self.start,
            "goal_node": self.goal,
            "algorithm_used": self.algorithm.value,
            "success": True
        }


def run_advanced_goal_based_agent_demo():
    """Demo function for the advanced goal-based agent."""
    # Define a more complex graph
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

    print("--- Advanced Goal-Based Agent Demo ---")
    print(f"Goal: Reach {GOAL_NODE}")
    print(f"Starting Point: {START_NODE}\n")

    # Create agent with default Dijkstra
    agent = AdvancedGoalBasedAgent(MAP_ROUTES, START_NODE, GOAL_NODE)
    best_plan, best_cost = agent.plan()

    print(f"Planning result: ")
    print(f"  - Best plan: {best_plan}")
    print(f"  - Total cost: {best_cost}")

    # Get detailed path information
    path_details = agent.get_path_details()
    print(f"\nDetailed path information:")
    print(f"  - Best path: {path_details['best_path']}")
    print(f"  - Best cost: {path_details['best_cost']}")
    print(f"  - Algorithm used: {path_details['algorithm_used']}")
    print(f"  - Alternative paths found: {len(path_details['all_alternative_paths'])}")
    
    for i, (path, cost) in enumerate(path_details['all_alternative_paths']):
        print(f"    Path {i+1}: {' -> '.join(path)} with cost {cost}")

    # Execute the first action if path exists
    if best_cost != float('inf'):
        # Extract the first destination from the path
        first_action_node = best_plan.split(' -> ')[1]

        print("\nExecuting first action...")
        print(f"Action taken: Move to {first_action_node}")
        print(f"(Agent continues following the rest of the plan to reach {GOAL_NODE})")
    else:
        print("\nAction taken: Cannot take action. Goal is unreachable.")


if __name__ == "__main__":
    run_advanced_goal_based_agent_demo()