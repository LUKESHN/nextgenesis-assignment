import json
import math
import csv

# Calculate Euclidean distance
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Read JSON file
with open("data.json", "r") as file:
    data = json.load(file)


warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]


# Create report structure
report = {}

for agent_id in agents:
    report[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0.0
    }


# Store packages assigned to each agent
assigned_packages = {}

for agent_id in agents:
    assigned_packages[agent_id] = []


# ------------------------------------------------
# STEP 1: Assign each package to nearest agent
# ------------------------------------------------

for package in packages:

    package_id = package["id"]
    warehouse_id = package["warehouse"]

    warehouse_location = warehouses[warehouse_id]

    nearest_agent = None
    shortest_distance = float("inf")

    for agent_id, agent_location in agents.items():

        d = distance(agent_location, warehouse_location)

        if d < shortest_distance:
            shortest_distance = d
            nearest_agent = agent_id

    assigned_packages[nearest_agent].append(package)


# ------------------------------------------------
# STEP 2: Simulate delivery
# ------------------------------------------------

for agent_id, agent_packages in assigned_packages.items():

    current_location = agents[agent_id]

    for package in agent_packages:

        warehouse_location = warehouses[package["warehouse"]]
        destination = package["destination"]

        # Agent travels to warehouse
        distance_to_warehouse = distance(
            current_location,
            warehouse_location
        )

        # Warehouse to destination
        delivery_distance = distance(
            warehouse_location,
            destination
        )

        # Add total distance
        report[agent_id]["total_distance"] += (
            distance_to_warehouse + delivery_distance
        )

        # Package delivered
        report[agent_id]["packages_delivered"] += 1

        # Agent is now at destination
        current_location = destination


# ------------------------------------------------
# STEP 3: Calculate efficiency
# ------------------------------------------------

for agent_id in report:

    packages_delivered = report[agent_id]["packages_delivered"]
    total_distance = report[agent_id]["total_distance"]

    if packages_delivered > 0:
        report[agent_id]["efficiency"] = (
            total_distance / packages_delivered
        )
    else:
        report[agent_id]["efficiency"] = 0


# ------------------------------------------------
# STEP 4: Find most efficient agent
# ------------------------------------------------
# Lower distance per package = better efficiency

agents_with_packages = [
    agent_id
    for agent_id in report
    if report[agent_id]["packages_delivered"] > 0
]

best_agent = min(
    agents_with_packages,
    key=lambda agent_id: report[agent_id]["efficiency"]
)

report["best_agent"] = best_agent


# Round numerical values
for agent_id in agents:

    report[agent_id]["total_distance"] = round(
        report[agent_id]["total_distance"], 2
    )

    report[agent_id]["efficiency"] = round(
        report[agent_id]["efficiency"], 2
    )


# ------------------------------------------------
# STEP 5: Save report
# ------------------------------------------------

with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# ------------------------------------------------
# STEP 6: Export top performer to CSV
# ------------------------------------------------

with open("top_performer.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "agent_id",
        "packages_delivered",
        "total_distance",
        "efficiency"
    ])
    # Top performer data
    writer.writerow([
        best_agent,
        report[best_agent]["packages_delivered"],
        report[best_agent]["total_distance"],
        report[best_agent]["efficiency"]
    ])
# Display result
print("FastBox Delivery Report")
print("-----------------------")

for agent_id in agents:

    print(
        agent_id,
        "Packages:",
        report[agent_id]["packages_delivered"],
        "Distance:",
        report[agent_id]["total_distance"],
        "Efficiency:",
        report[agent_id]["efficiency"]
    )

print("Best Agent:", report["best_agent"])

print("\nReport saved successfully as report.json")
print("Top performer saved successfully as top_performer.csv")