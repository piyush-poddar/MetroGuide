"""
Module for various mappings.
"""
import json
from collections import defaultdict

metro = "dmrc"
with open(rf"{metro}\line_wise_station_details.json", "r") as stations_file:
    stations = json.load(stations_file)

# code_name = dict()
name_code = dict()
id_code = dict()
# code_id = dict()
id_line = defaultdict(list)
name_id = dict()
id_name = dict()

for metro_line in stations:
    for station in stations[metro_line]:
        # code_name[station["station_code"]] = station["station_name"]
        name_code[station["station_name"]] = station["station_code"]
        id_code[station["id"]] = station["station_code"]
        # code_id[station["station_code"]] = station["id"]

        name_id[station["station_name"]] = station["id"]
        id_name[station["id"]] = station["station_name"]
        id_line[station["id"]].append(metro_line)


with open(rf"{metro}\name_to_id.json", "w") as name_id_file:
    json.dump(name_id, name_id_file, indent=4)

with open(rf"{metro}\id_to_name.json", "w") as id_name_file:
    json.dump(id_name, id_name_file, indent=4)

# with open(rf"{metro}\code_to_name.json", "w") as code_name_file:
#     json.dump(code_name, code_name_file, indent=4)

with open(rf"{metro}\name_to_code.json", "w") as name_code_file:
    json.dump(name_code, name_code_file, indent=4)

with open(rf"{metro}\id_to_code.json", "w") as id_code_file:
    json.dump(id_code, id_code_file, indent=4)

# with open(rf"{metro}\code_to_id.json", "w") as code_id_file:
#     json.dump(code_id, code_id_file, indent=4)

with open(rf"{metro}\id_to_line.json", "w") as id_line_file:
    json.dump(id_line, id_line_file, indent=4)