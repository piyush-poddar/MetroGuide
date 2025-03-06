import json
import requests
from datetime import datetime
import time
from collections import defaultdict
import os

metro = "dmrc"
with open(os.path.join(metro, "line_wise_station_details.json"), "r") as line_wise_stations_file:
    line_wise_stations = json.load(line_wise_stations_file)

no_of_stations = len(set([station["id"] for metro_line in line_wise_stations 
                          for station in line_wise_stations[metro_line]]))
print(no_of_stations)

metro_graph = defaultdict(list)
a = time.time()
for metro_line in line_wise_stations:
    for station_index in range(len(line_wise_stations[metro_line])-1):
        src_id = int(line_wise_stations[metro_line][station_index]["id"])
        dest_id = int(line_wise_stations[metro_line][station_index+1]["id"])
        src_code = line_wise_stations[metro_line][station_index]["station_code"]
        dest_code = line_wise_stations[metro_line][station_index+1]["station_code"]

        base_url = f"https://backend.delhimetrorail.com/api/v2/en/station_route/{src_code}/{dest_code}/least-distance"
        url = f"{base_url}/{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}"
        print(metro_line, base_url)
        route = requests.get(url).json()
        total_time = route["total_time"]
        h, m, s = map(int, total_time.split(":"))
        total_time_in_seconds = h * 60 * 60 + m * 60 + s

        # Adding Edge in graph
        metro_graph[src_id].append([dest_id, total_time_in_seconds])
        metro_graph[dest_id].append([src_id, total_time_in_seconds])

        #print(src_code, dest_code, total_time)
        #print()
        # Remove break
        break
    # Remove break
    break

b = time.time()
print(b-a)

# Run after removing break statements
# with open(os.path.join(metro, "graph.json"), "w") as graph_file:
#     json.dump(metro_graph, graph_file, indent=4)