import json
import sys
import difflib
import pandas 

old = sys.argv[1] 
new = sys.argv[2]

new_package_df = pandas.read_excel(new, sheet_name="Package netlist",na_filter=False)

f = open("new_out.json", "w")
f.write(new_package_df.to_json(orient='records'))
file = open("new_out.json")
new_package_data = json.load(file)
file.close()

file = open(old)
old_package_data = json.load(file)
file.close()

file = open("diff.txt", "w")
# for row in new_package_data:
#     i = 0
#     if row["Ballout Number"] == None:
#         continue
#     for row2 in old_package_data:
#         if row["Ballout Number"] == row2["Ballout Number"]:
#             break
#         if i == len(row2):
#             file.write(json.dumps(row, indent=4))
#         i+=1

diff = 0 

for i in range(1,len(new_package_data)):
    c = i + diff
    if old_package_data[c]["Pin Number"] != new_package_data[i]["Pin Number"] and old_package_data[c]["Net Name (Ballout)"] != new_package_data[i]["Net Name (Ballout)"]:
        diff -= 1
        file.write(json.dumps(new_package_data[i], indent=4))

file.close()