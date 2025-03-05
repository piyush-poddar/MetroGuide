import json
import heapq
from collections import defaultdict

metro = 'dmrc'
with open(rf"{metro}\graph.json") as graph_file:
    graph = json.load(graph_file)
graph = {int(vertex):edges for vertex, edges in graph.items()}

with open(rf"{metro}\id_to_line.json") as id_line_file:
    id_line = json.load(id_line_file)

with open(rf"{metro}\id_to_name.json") as id_name_file:
    id_name = json.load(id_name_file)

with open(rf"{metro}\name_to_id.json") as name_id_file:
    name_id = json.load(name_id_file)

with open(rf"{metro}\interchange_details.json") as interchange_file:
    interchange = json.load(interchange_file)

with open(rf"{metro}\lines.json") as line_details_file:
    line_details = json.load(line_details_file)

def dijkstra(start, end):
    # Initialize distances and path tracking
    distances = {vertex: float('infinity') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = 0
    
    # Priority queue to select the vertex with the minimum distance
    priority_queue = [(0, start)]
    
    while priority_queue:
        # Pop the vertex with the smallest distance
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Early exit if we reach the destination
        if current_vertex == end:
            break
        
        # If the popped vertex has a larger distance than the recorded distance, skip it
        if current_distance > distances[current_vertex]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # If a shorter path to neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Reconstruct the shortest path by backtracking from the destination
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path = path[::-1]  # Reverse the path to start from the source
    
    # Check if there's a valid path
    if distances[end] == float('infinity'):
        return float('infinity'), []  # No path found
    else:
        return distances[end], path

def get_route(start, end):
    total_time, route = dijkstra(start, end)
    cur_line = list(set(id_line[str(route[0])]).intersection(set(id_line[str(route[1])])))[0]
    complete_route = defaultdict()
    complete_route["total_time"] = total_time
    complete_route["route"] = []
    complete_route["route"].append({"line_code":cur_line,
                                    "line":line_details[cur_line]["line_color"], 
                                    "line_color":line_details[cur_line]["primary_color_code"],
                                    "path":[]})
    
    for stn_id in route:
        if complete_route["route"][-1]["line_code"] not in id_line[str(stn_id)]:
            cur_line = id_line[str(stn_id)][0]
            old_line = complete_route["route"][-1]["line_code"]
            interchange_stn_id = name_id[complete_route["route"][-1]["path"][-1]]
            complete_route["total_time"]+=interchange[old_line][cur_line][str(interchange_stn_id)]*60
            complete_route["route"].append({"line_code":cur_line,
                                    "line":line_details[cur_line]["line_color"], 
                                    "line_color":line_details[cur_line]["primary_color_code"],
                                    "path":[complete_route["route"][-1]["path"][-1], id_name[str(stn_id)]]})
        else:
            complete_route["route"][-1]["path"].append(id_name[str(stn_id)])
    
    return dict(complete_route)

if __name__=='__main__':
    start_vertex = 202
    end_vertex = 141
    complete_route = get_route(start_vertex, end_vertex)
    print(complete_route)