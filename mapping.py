import json
import pandas
import sys

from v2.0.temppython import n7_ball_match


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

output_data = []

#############################################################################################
#               logic code below                                                            #
#############################################################################################


#TODO#
#CODE HERE#
i = 0
for pin in n7_pinsheet_data:
    for ballout in balloutsheet_data:
        for x,y in ballout.items():
            #TODO#
            #Talk to jason about what implicit means in terms of the ballout.#
            #   because i believe i will need to consult that list first before proceeding with the following steps 
            #   PLACEHOLDER   #
            
            #PART (A)#
            #match die and ballout#
            if(pin[name_net_name_die] == y):
                #define ballout number values#
                pin_number = pin["Pin Number"]
                net_name_N7 = pin["Net Name"]
                net_name_C4 = y
                net_name_Ballout = y
                x_N7 = pin["X Coord (design)"]
                y_N7 = pin["Y Coord (design)"]
                x_C4 = pin["X  Coord (C4 Bump)"]        #?
                y_C4 = pin["Y  Coord (C4 Bump)"]        #?
                ballout_number = ballout_number
                ballout_x_value =  int(x) - 1 # int(x) - 1 was the previous values
                ballout_y_value = ballout["Unnamed: 0"]
                #must decide how this is going to be created ...
                ballout_number = "{}{}".format(ballout_y_value,ballout_x_value)
                row =n7_ball_match(pin_number, net_name_N7, net_name_C4, net_name_Ballout, x_N7, y_N7, x_C4, y_C4, ballout_number)
                output_data.append(row)
    i =+ 1 

            #PART (B)#
            #match die and hbm3 

    for mem in hbm3_pinsheet_data:
        if pin["Net Name"] == mem["Net Name"]:
            
            #PART (C)#
            #match hbm3 and ballout ##IFF## the pin was not matched to die
        #elif...


print(output_data)



#############################################################################################
#               more file creation                                                          #
#############################################################################################

# with open("output.json", "w") as output: 
#     json.dump(pinsheet_data, output)


##NEED TO CHANGE THIS....
##  RN THIS JUST DUMPS THE INPUT PINSHEET DATA TO THE OUT..
##  CREATE NEW JSON AND DUMP THAT TO DF ##

# df = pandas.DataFrame(data=pinsheet_data)
# df.to_excel("outputsept27.xlsx", index=False,freeze_panes=(1,0))