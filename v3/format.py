import sys
import json
import pandas

#needs to be tested#



#######################################################################################
#       c4 format                                                                     #
#######################################################################################

ballout_xl = sys.argv[2]

ballout_netlist = []

#create json to store information
f = open("balloutsheet.json","w")

#extract xl data to dataframe (pandas)
ballout_sheet_df = pandas.read_excel(ballout_xl,header=1)

#write dataframe to json 
f.write(ballout_sheet_df.to_json(orient='records'))

#load json (json --> python dict)
file=open('balloutsheet.json')
balloutsheet_data = json.load(file)
file.close()


#######################################################################################

#ballout template: 

bo_template = {
    "ballout_name" : None,
    "ballout_number" : None,
    "matched" : None,
    "power" : None
}



for ballout in balloutsheet_data:
    for x,y in ballout.items():
        #possible forcefully skip "Unnamed: 0"
        if x == "Unnamed: 0" or x == "Unnamed: 1":
            continue
        new_bo_cell = dict.fromkeys(bo_template,None)   #create empty cell to populate in logic below 
        #IF(power signal) THEN: label power and label matched 1 (?)
        new_bo_cell["ballout_name"] = y
        ballout_x_value = int(x)                      
        ballout_y_value = ballout["Unnamed: 1"]       
        ballout_number = "{}{}".format(ballout_y_value, ballout_x_value)
        new_bo_cell["ballout_number"] = ballout_number
        ballout_netlist.append(new_bo_cell)


#######################################################################################
#       n7 format                                                                     #
#######################################################################################

n7_xl = sys.argv[1]

n7_out_data = []

#create json to store information
f = open("n7_pinsheet.json","w")

#extract xl data to dataframe (pandas)
n7_pinsheet_df = pandas.read_excel(n7_xl,header=1)

#write dataframe to json 
f.write(n7_pinsheet_df.to_json(orient='records'))

#load json (json --> python dict)
file=open('n7_pinsheet.json')
n7_pinsheet_data = json.load(file)
file.close()


#######################################################################################

#ballout template: 

n7_template = {
    "Pin Number" : None,
    "Net Name (ubmp N7 die)" : None,
    "N7 die (Interposer Loopback)" : None,
    "Net Name (ubmp HBM3 DRAM)" : None,
    "Net Name (C4 Bump)" : None,
    "Net Name (Ballout)" : None,
    "X Coord (N7 ubmp)" : None,
    "Y Coord (N7 ubmp)" : None,
    "X Coord (Interposer Loopback)" : None,
    "Y Coord (Interposer Loopback)" : None,
    "X Coord (HBM3 ubmp)" : None,
    "Y Coord (HBM3 ubmp)" : None,
    "X Coord (C4 Bump)" : None,
    "Y Coord (C4 Bump)" : None,
    "Ballout Number" : None
}



def make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(n7_template, "N/A") #create new dictionary from template (template_data is the json.load(file) of template.json)
    new_dict_element["Pin Number"] = pin_number
    new_dict_element["Net Name (ubmp N7 die)"] = net_name_N7
    new_dict_element["Net Name (ubmp HBM3 DRAM)"] = net_name_HBM3
    new_dict_element["Net Name (C4 Bump)"] = net_name_C4
    new_dict_element["Net Name (Ballout)"] = net_name_Ballout
    new_dict_element["X Coord (N7 ubmp)"] = x_N7
    new_dict_element["Y Coord (N7 ubmp)"] = y_N7
    new_dict_element["X Coord (HBM3 ubmp)"] = x_HBM3
    new_dict_element["Y Coord (HBM3 ubmp)"] = y_HBM3
    new_dict_element["X Coord (C4 Bump)"] = x_C4
    new_dict_element["Y Coord (C4 Bump)"] = y_C4
    new_dict_element["Ballout Number"] = ballout_number
    n7_out_data.append(new_dict_element)


for pin in n7_pinsheet_data:
        pin_number = pin["Pin Number"]
        net_name_N7 = pin["Net Name"]
        net_name_HBM3 = "N/A"
        net_name_C4 = "N/A"
        net_name_Ballout = "N/A"
        x_N7 = pin["X Coord (design)"]
        y_N7 = pin["Y Coord (design)"]
        x_HBM3 = "N/A"
        y_HBM3 = "N/A"
        x_C4 = None
        y_C4 = None
        ballout_number = "N/A"
        make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number)

#intermediate save of n7_out_data
out_file = open("n7_output.json", "w")
json.dump(n7_out_data, out_file)
out_file.close()





###output options###
# configure to interface with mapping.py
# uncomment selection

#c4#
#to json 
out_file = open("ballout_formatted.json", "w")
json.dump(ballout_netlist, out_file)
out_file.close()

# to excel
#df = pandas.DataFrame(data=ballout_netlist)




