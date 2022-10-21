import json
import pandas
import sys



if len(sys.argv) == 4:
    n7_pinsheet_xl = sys.argv[1]
    ballout_xl = sys.argv[2]
    hbm3_pinsheet_xl = sys.argv[3]
else:
    print("must hardcode this...")
    exit()



#############################################################################################
#           Hardcode the implicit mappings here                                             #
#############################################################################################


#TODO#
#   VERIFY  #
#   FORMALIZE PROCESS   #
#   RENAME  #

implicit = {
    "GD" : "VSS",
    "PWR18" : "VDD18",
    "PWRIOC" : "VDDIO_OPHY",
    "PWRIOC_GPIO" : "VDD_GPIO",
    "PWRIOC_TST" : "VDDIO_TST",
    "PWRIOH" : "VDDQ_OPHY",
    "PWRIOH_GPIO" : "VDD18",
    "PWRIOH_TST" : "VDDQ_TST", 
    "PWRIOL" : "VDDQL_OPHY",
    "PWRIOL_TST" : "VDDQL_TST"
}

#EXCEL COLUMN NAMES#
#   define variables that can easily be changed to handle inconsistencies with varying input files   #
#       always use these variables when addressing the json items to keep it easily changable        #
name_net_name_die = "Net Name (ubmp N7 die)"
name_net_name_ballout = "Net Name (Ballout)"
name_net_name_bump = "Net Name (C4 Bump)"
name_ballout_number = "Ballout Number"




#############################################################################################


f = open("n7_pinsheet.json", "w")
x = open("balloutsheet.json", "w")
y = open("hbm3_pinsheet.json", "w")



#############################################################################################
#   change the sheet_name of each to support multi sheet excel                              #
#############################################################################################

ballout_sheet_df = pandas.read_excel(ballout_xl,header=1)
n7_pin_sheet_df = pandas.read_excel(n7_pinsheet_xl)
hbm3_pin_sheet_df = pandas.read_excel(hbm3_pinsheet_xl)
#############################################################################################

print(ballout_sheet_df)

f.write( n7_pin_sheet_df.to_json(orient='records'))
file = open('n7_pinsheet.json')
n7_pinsheet_data = json.load(file)
file.close()

x.write( ballout_sheet_df.to_json(orient='records'))
file = open('balloutsheet.json')
balloutsheet_data = json.load(file)
file.close()

y.write( hbm3_pin_sheet_df.to_json(orient='records'))
file = open('hbm3_pinsheet.json')
hbm3_pinsheet_data = json.load(file)
file.close()

file = open('cell_template.json')
template_data = json.load(file)
file.close()
n7_out_data = []
hbm_extras_data = []

#############################################################################################
#               supporting functions                                                            #
#############################################################################################

def n7_ball_match(pin_number, net_name_N7, net_name_C4, net_name_Ballout, x_N7, y_N7, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(template_data,"N/A") #create new dictionary from template (template_data is the json.load(file) of template.json)
    new_dict_element["Pin Number"] = pin_number
    new_dict_element["Net Name (ubmp N7 die)"] = net_name_N7
    new_dict_element["Net Name (C4 Bump)"] = net_name_C4
    new_dict_element["Net Name (Ballout)"] = net_name_Ballout
    new_dict_element["X Coord (N7 ubmp)"] = x_N7
    new_dict_element["Y Coord (N7 ubmp)"] = y_N7
    new_dict_element["X Coord (C4 Bump)"] = x_C4
    new_dict_element["Y  Coord (C4 Bump)"] = y_C4
    new_dict_element["Ballout Number"] = ballout_number
    return new_dict_element


def make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(template_data, None) #create new dictionary from template (template_data is the json.load(file) of template.json)
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

def make_cell_hbm(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(template_data, None) #create new dictionary from template (template_data is the json.load(file) of template.json)
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
    hbm_extras_data.append(new_dict_element)

#############################################################################################
#               logic code below                                                            #
#############################################################################################

##create new dict in wanted format##
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
        x_C4 = "N/A"
        y_C4 = "N/A"
        ballout_number = None
        make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number)

out_file = open("n7_output.json", "w")
json.dump(n7_out_data, out_file)
out_file.close()


## scan new dict and fill out matches from ballout ##

for pin in n7_out_data:
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            if( implicit.get( pin["Net Name (ubmp N7 die)"] , 'missing') != 'missing'  ):
                #find matches with implied connections#
                pin["Net Name (C4 Bump)"] = implicit[pin["Net Name (ubmp N7 die)"]]
                pin["Net Name (Ballout)"] = implicit[pin["Net Name (ubmp N7 die)"]]
                pin["Ballout Number"] = "N/A"
            elif pin["Net Name (ubmp N7 die)"] == y and y != None:
                ballout_x_value = int(x)                       ###*****####
                ballout_y_value = ballout["Unnamed: 1"]        ###*****####  ALSO CHANGE IN ADD RELATION ()
                ballout_number = "{}{}".format(ballout_y_value, ballout_x_value)
                pin["Ballout Number"] = ballout_number
                pin["Net Name (C4 Bump)"] = y
                pin["Net Name (Ballout)"] = y  

#############################################################################################
#       HANDLE IMPLICIT RELATIONS HERE                                                      #
#############################################################################################
def create_element(nn_d, nn_b, ballout_num):
    new_dict_element = dict.fromkeys(template_data,None)
    new_dict_element["Net Name (ubmp N7 die)"] = nn_d
    new_dict_element["Pin Number"] = "N/A"
    new_dict_element["Net Name (Ballout)"] = nn_b
    new_dict_element["Net Name (C4 Bump)"] = nn_b
    new_dict_element["Ballout Number"] = ballout_num
    new_dict_element["Net Name (ubmp HBM3 DRAM)"]= "N/A"
    return new_dict_element
                
def add_relation(NN_D, NN_BO, i):
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            if NN_BO == y:
                ballout_x_value = int(x) 
                ballout_y_value = ballout["Unnamed: 1"]
                new_element = create_element(NN_D, NN_BO, "{}{}".format(ballout_y_value , ballout_x_value))
                n7_out_data.insert(i, new_element)


i = 0
for pin in n7_out_data:
    if( implicit.get( pin["Net Name (ubmp N7 die)"] , 'N/A') != 'N/A'  ):
        add_relation(pin["Net Name (ubmp N7 die)"], implicit[ pin["Net Name (ubmp N7 die)"] ], i)
        implicit.pop(pin["Net Name (ubmp N7 die)"])
    i += 1


#############################################################################################
#           deal with hbm3 - n7 relations (may need to move the order)                      #
#############################################################################################
t=0
for mem in hbm3_pinsheet_data:
    for pin in n7_out_data:
        if pin["Net Name (ubmp N7 die)"] == mem["Net Name"] and mem["Net Name"] != "VSS":
            pin["Net Name (ubmp HBM3 DRAM)"] = mem["Net Name"]
            pin["X Coord (HBM3 ubmp)"] = mem["X Coord (design)"]
            pin["Y Coord (HBM3 ubmp)"] = mem["Y Coord (design)"]
            mem["Pin Number"] = "x"
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            if mem["Net Name"] == y and mem["Pin Number"] != "x" and y != "VSS":
                pin_number = None
                net_name_N7 = "N/A"
                net_name_HBM3 = mem["Net Name"]
                net_name_C4 = mem["Net Name"]
                net_name_Ballout = mem["Net Name"]
                x_N7 = "N/A"
                y_N7 = "N/A"
                x_HBM3 = mem["X Coord (design)"]
                y_HBM3 = mem["Y Coord (design)"]
                x_C4 = None
                y_C4 = None
                ballout_x_value = int(x)                       ###*****####
                ballout_y_value = ballout["Unnamed: 1"]   
                ballout_number = "{}{}".format(ballout_y_value,ballout_x_value)
                make_cell_hbm(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number)
    
# for mem in hbm3_pinsheet_data:
#     mem["Pin Number"] = None
#############################################################################################
#           output to file                      
#############################################################################################

# out_file = open("n7_output.json", "w")
# json.dump(n7_out_data, out_file)
# out_file.close()

df = pandas.DataFrame(data=n7_out_data)
df.to_excel("n7_output_xl.xlsx", index=False, freeze_panes=(1,0))

df = pandas.DataFrame(data=hbm_extras_data)
df.to_excel("hbm3_mappings_to_ballout.xlsx", index=False, freeze_panes=(1,0))