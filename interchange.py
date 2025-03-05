import json
import requests
import time
from datetime import datetime
from collections import defaultdict

metro = "dmrc"

with open(rf"{metro}\line_wise_station_details.json", "r") as line_wise_stations_file:
    line_wise_stations = json.load(line_wise_stations_file)

def fetch_route(src_code, dest_code):
    print(src_code, dest_code)
    base_url = f"https://backend.delhimetrorail.com/api/v2/en/station_route/{src_code}/{dest_code}/least-distance"
    url = f"{base_url}/{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}"
    route = requests.get(url).json()["route"]
    return route   
          
tree = lambda: defaultdict(tree) # For nested defaultdict
interchange_data = tree()

for metro_line in line_wise_stations:
    for station in line_wise_stations[metro_line]:
        if station["interchange"] == True:
            stn_ind_lin1 = line_wise_stations[metro_line].index(station)
            for other_metro_line in line_wise_stations:
                if other_metro_line!=metro_line:
                    if station in line_wise_stations[other_metro_line]:
                        stn_ind_lin2 = line_wise_stations[other_metro_line].index(station)
                        f1 = stn_ind_lin1!=0
                        f2 = stn_ind_lin2!=0
                        f3 = stn_ind_lin1!=len(line_wise_stations[metro_line])-1
                        f4 = stn_ind_lin2!=len(line_wise_stations[other_metro_line])-1
                        if f1 and f2:
                            src_code = line_wise_stations[metro_line][stn_ind_lin1-1]["station_code"]
                            dest_code = line_wise_stations[other_metro_line][stn_ind_lin2-1]["station_code"]
                            if src_code!=dest_code:
                                route = fetch_route(src_code, dest_code)
                                if len(route)==2:
                                    interchange_data[metro_line][other_metro_line][station["id"]] = route[1]["station_interchange_time"]
                                    continue
                        if f1 and f4:
                            src_code = line_wise_stations[metro_line][stn_ind_lin1-1]["station_code"]
                            dest_code = line_wise_stations[other_metro_line][stn_ind_lin2+1]["station_code"]
                            if src_code!=dest_code:
                                route = fetch_route(src_code, dest_code)
                                if len(route)==2:
                                    interchange_data[metro_line][other_metro_line][station["id"]] = route[1]["station_interchange_time"]
                                    continue
                        if f2 and f3:
                            src_code = line_wise_stations[metro_line][stn_ind_lin1+1]["station_code"]
                            dest_code = line_wise_stations[other_metro_line][stn_ind_lin2-1]["station_code"]
                            if src_code!=dest_code:
                                route = fetch_route(src_code, dest_code)
                                if len(route)==2:
                                    interchange_data[metro_line][other_metro_line][station["id"]] = route[1]["station_interchange_time"]
                                    continue
                        if f3 and f4:
                            src_code = line_wise_stations[metro_line][stn_ind_lin1+1]["station_code"]
                            dest_code = line_wise_stations[other_metro_line][stn_ind_lin2+1]["station_code"]
                            if src_code!=dest_code:
                                route = fetch_route(src_code, dest_code)
                                if len(route)==2:
                                    interchange_data[metro_line][other_metro_line][station["id"]] = route[1]["station_interchange_time"]
                                    continue

with open(rf"{metro}\interchange_details.json", "w") as interchange_details_file:
    json.dump(interchange_data, interchange_details_file, indent=4)