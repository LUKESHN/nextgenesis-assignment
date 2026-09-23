# nextgenesis-assignment
## Assumptions & Engineering Decisions

To handle scenarios that are not explicitly defined in the project requirements, the following logical assumptions were made:

1. Nearest Agent Assignment
   Each package is assigned to the available delivery agent with the shortest Euclidean distance from the package location.

2. Distance Calculation
   Euclidean distance is used because the input data provides coordinate-based locations.
   Formula:
   `Distance = √((x2 - x1)² + (y2 - y1)²)`

3. Tie-Breaking
   If two agents have the same distance from a package, the agent with fewer currently assigned packages is selected. If the workload is also equal, the agent ID is used as the final tie-breaker.

4. Delivery Order
   Packages assigned to an agent are delivered in the order in which they are assigned. This keeps the simulation simple and deterministic.

5. Agent Availability
   An agent can receive a new package only if the agent is available for delivery.

6. New Agent Joining Mid-Day
   A new agent becomes available from the specified joining time and can receive packages from that point onward.

7. Delivery Delay
   A random delay is generated for deliveries to simulate realistic operational conditions. The delay is recorded in the final report.

8. Failed or Invalid Data
   Invalid or incomplete input records are handled safely where possible, and the program avoids crashing because of a single invalid record.

9. Package Delivery
   A package is considered successfully delivered when the assigned agent completes its simulated route.

10. Top Performer
    The top performer is determined using the number of successfully delivered packages. Total distance and delivery delays are also recorded for performance analysis.

11. Route Visualization
    ASCII routes are used to provide a simple text-based representation of warehouse, agent, and package movement without requiring external visualization libraries.

12. Output Files
    The simulation generates `report.json` containing the complete results and `top_performer.csv` containing the top-performing agent's details.

13. Reproducibility
    Random delivery delays may produce different results on different executions. A random seed can be used when reproducible results are required.

These assumptions were selected to keep the simulation logical, efficient, deterministic where possible, and easy to understand while allowing the system to handle undefined scenarios without manual intervention.
