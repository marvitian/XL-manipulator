import sys
import json
import pandas


if len(sys.argv) == 3:
    pinsheet_xl = sys.argv[1]
    ballout_xl = sys.argv[2]
else:
    print("must hardcode this...")
    exit()



#############################################################################################
#           Hardcode the implicit mappings here                                             #
#############################################################################################


#TODO#
implicit = {
    "GD" : "VSS",
    "VDD" : "VDD",
    "VSS" : "VSS",
    "PWR18" : "VDD18",
    "PWRIOC" : "VDDIO_OPHY",
    "PWRIOC_GPIO" : "VDD_GPIO",
    "PWRIOC_TST" : "VDDIO_TST",
    "PWRIOH" : "VDDQ",
    "PWRIOH_GPIO" : "VDD18",
    "PWRIOH_TST" : "VDDQ_TST", 
    "PWRIOL" : "VDDQL_OPHY",
    "PWRIOL_TST" : "VDDQL_TST"
}


#############################################################################################






f = open("pinsheet.json", "w")
x = open("balloutsheet.json", "w")
#############################################################################################
#   change the sheet_name of each to support multi sheet excel                              #
#############################################################################################


ballout_sheet_df = pandas.read_excel(ballout_xl,header=1)
pin_sheet_df = pandas.read_excel(pinsheet_xl)
#############################################################################################

print(ballout_sheet_df)

f.write( pin_sheet_df.to_json(orient='records'))

file = open('pinsheet.json')
pinsheet_data = json.load(file)
file.close()

x.write( ballout_sheet_df.to_json(orient='records'))
file = open('balloutsheet.json')
balloutsheet_data = json.load(file)
file.close()


#############################################################################################
#               logic code below                                                            #
#############################################################################################

# 1.	Pin Number
    # a.	Same as pin number in TSMC N7 Die Netlist
    # b.	N/A for all the power/grounds as before

# 2.	Die
    # a.	Just fill in “N7 Die” for anything that has a pin number (exists in TSMC N7 die netlist)
for pin in pinsheet_data:                           #fill the table before additions are made
    pin["Die"]="N7 Die"
    pin["Bump X Coord"] = "N/A"
    pin["Bump Y Coord"] = "N/A"
    
# 3.	Netname (Die)
    # a.	Same as before matching with the die netlist name even if the Pin Number is N/A

# 4.	X Coord/Y Coord
    # a.	Same as before.  If it is in the TSMC N7 die netlist then just copy over

    
# 5.	Net Name (Bump)
    # a.	Same as before.  Copy the Ballout name.  If the ballout name is N/A, then this will also be N/A

# 6.	Bump X(Y) Coord
    # a.	Same as before.  If it is in both the TSMC N7 die netlist and the ballout then leave blank
    # b.	Otherwise N/A
    
# 7.	Net Name (Ballout)
    # a.	Same as before.  Use the power mappings as before
    
    
# 8.	Ballout Number
    # a.	Same as before. 

for pin in pinsheet_data:
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            if( implicit.get( pin["Net Name (Die)"] , 'N/A') != 'N/A'  ):
                #if this pin exists in the implicit net name include the corresponding data in the output
                #use .get to make these fields optional 

                if(pin.get("Net Name (Bump)", "N/A") != "N/A"):
                    pin["Net Name (Bump)"]=implicit[pin["Net Name (Die)"]]
                if(pin.get("Net Name (Ballout)", "N/A") != "N/A"):
                    pin["Net Name (Ballout)"]=implicit[pin["Net Name (Die)"]]
                if(pin.get("Ballout Number", "N/A") != "N/A"):
                    pin["Ballout Number"] = "N/A"

            elif pin["Net Name (Die)"] == y:
                #find matches in ballout
                ballout_x_value = int(x) - 1                                     ##might need to adjust from run to run 
                pin["Ballout Number"] = "{}{}".format(ballout["Unnamed: 0"] , ballout_x_value)
                pin["Net Name (Ballout)"] = y
                pin["Net Name (Bump)"] = y
                pin["Bump X Coord"] = None
                pin["Bump Y Coord"] = None
            # else:
            #     pin["Net Name (Ballout)"] = "N/A"
            #     pin["Net Name (Bump)"] = "N/A"
            #     pin["Ballout Number"] = "N/A"
            #     pin["Bump X Coord"] = "N/A"
            #     pin["Bump Y Coord"] = "N/A"
            


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#@              functions for implicit mappings                                            @#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def create_element(nn_d, nn_b, ballout_num):
    new_dict_element = dict.fromkeys(pinsheet_data[0],"N/A")
    new_dict_element["Net Name (Die)"] = nn_d
    new_dict_element["Die"] =None
    new_dict_element["Pin Number"] = "N/A"
    if(new_dict_element.get("Net Name (Ballout)", "missing") != "missing"):
        new_dict_element["Net Name (Ballout)"] = nn_b
    if(new_dict_element.get("Net Name (Bump)", "missing") != "missing"):
        new_dict_element["Net Name (Bump)"] = nn_b
    new_dict_element["Ballout Number"] = ballout_num
    return new_dict_element

def add_relation(NN_D, NN_BO, i):
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            if NN_BO == y:
                ballout_x_value = int(x) - 1
                new_element = create_element(NN_D, NN_BO, "{}{}".format(ballout["Unnamed: 0"] , ballout_x_value))
                pinsheet_data.insert(i, new_element)



i = 0
for pin in pinsheet_data:
    if( implicit.get( pin["Net Name (Die)"] , 'N/A') != 'N/A'  ):
        add_relation(pin["Net Name (Die)"], implicit[ pin["Net Name (Die)"] ], i)
        implicit.pop(pin["Net Name (Die)"])
    i += 1


#############################################################################################
#               more file creation                                                          #
#############################################################################################

with open("outputsept27.json", "w") as output: 
    json.dump(pinsheet_data, output)




df = pandas.DataFrame(data=pinsheet_data)
df.to_excel("outputsept27.xlsx", index=False,freeze_panes=(1,0))