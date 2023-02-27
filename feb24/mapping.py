import json
import sys
import pandas
import re
#argv 1 2 3 (from format.py) n7_out_data.json , ballout_formatted.json , hbm3_xl(for now, will be json later)


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

out_file = open("ballout_formatted.json", "w")
json.dump(ballout_netlist, out_file)
out_file.close()


#######################################################################################
#       n7 format                                                                     #
#######################################################################################

n7_xl = sys.argv[1]

n7_out_data = []

#create json to store information
f = open("n7_pinsheet.json","w")

#extract xl data to dataframe (pandas)
n7_pinsheet_df = pandas.read_excel(n7_xl)

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

#####################################################################################################
#####################################################################################################
#####################################################################################################

###pull in hbm3 netlist as json
hbm3_pinsheet_xl = sys.argv[3]
hbm3_pin_sheet_df = pandas.read_excel(hbm3_pinsheet_xl)

y = open("hbm3_pinsheet.json", "w")
y.write( hbm3_pin_sheet_df.to_json(orient='records'))
file = open('hbm3_pinsheet.json')
hbm3_pinsheet_data = json.load(file)
file.close()

# review before each run

implicit = {
    "GD" : "VSS",
    "PWR18" : "VDD18",
    "PWRIOC" : "VDDIO_OPHY",
    "PWRIOC_GPIO" : "VDD_GPIO",
    "PWRIOC_TST" : "VDDIO_TST",
    "PWRIOH" : "VDDQ_OPHY",
    "PWRIOH_GPIO" : "VDDQ_OPHY",
    "PWRIOH_TST" : "VDDQ_TST", 
    "PWRIOL" : "VDDQL_OPHY",
    "PWRIOL_TST" : "VDDQL_TST"
}

power = {
    "VSS" : "VSS",
    "VDDC" : "VDDC",
    "VDDQ" : "VDDQ",
    "VDDQL" : "VDDQL",
    "VPP" : "VPP"
}

# signals of the format <name><letter>
list1 = {
    "AERR" : "true",
    "APAR" : "true",
    "ARFU" : "true",
    "ATST" : "true",
    "RA" : "true",
    "WSO" : "true"
}

# signals of the format <name><letter><number>
list2 = {
    "C" : "true",
    "DBI" : "true",
    "DERR" : "true",
    "DPAR" : "true",
    "DQ" : "true",
    "ECC" : "true",
    "R" : "true",
    "RD" : "true",
    "SEV" : "true" 
}

# SIGNALS OF THE FORM <name><letter><number?>_<c or t> 
list3 = {
    "RDSQS" : "true",
    "WDQS" : "true",
    "CK" : "true" 
}

# new mapping   
letter_match = {
    "h" : "d",
    "d" : "h",
    "p" : "l",
    "l" : "p"
}
##load json into python library:
manual_exclusion = {
    "CptDrExt" : "true"
}

file = open("ballout_formatted.json")
c4_data = json.load(file)
file.close()



log = open("catch.log", "w")

def check_signal_mapping_swap(temp_pin):
    if(manual_exclusion.get(temp_pin, 'missing') != 'missing'):
        return False
    else:
        x = re.search("\A[A-Z]+", temp_pin)
        y = re.search("[a-z]", temp_pin)
        z1 = re.search("[0-9]+", temp_pin)
        z2 = re.search("[0-9]*[_][ct]?", temp_pin)
        print(temp_pin)
        if(x != None):
            x = x.group()
        if(list1.get(x, 'missing') != 'missing') or (list2.get(x, 'missing') != 'missing') or (list3.get(x, 'missing') != 'missing'):
            
            if(list1.get(x, 'missing') != 'missing'):
                print('success')
                if(letter_match.get(y.group(), 'missing') != 'missing'):
                    print("new maptemp_ping")
                    temp = "{}{}".format(x,letter_match[y.group()])
                    print(temp)
                else:
                    print("not new maptemp_ping")
                    temp = "{}{}".format(x, y.group())

            elif(list2.get(x, 'missing') != 'missing'):
                print('success 2')
                if(letter_match.get(y.group(), 'missing') != 'missing'):
                    print("new maptemp_ping")
                    temp = "{}{}{}".format(x, letter_match[y.group()], z1.group())
                    print(temp)
                else:
                    print("not new maptemp_ping")
                    temp = "{}{}{}".format(x, y.group(), z1.group())
                    print(temp)

            elif(list3.get(x, 'missing') != 'missing'):
                print('success 2')
                if(letter_match.get(y.group(), 'missing') != 'missing'):
                    print("new maptemp_ping")
                    temp = "{}{}{}".format(x, letter_match[y.group()], z2.group())
                    print(temp)
                else:
                    print("not new maptemp_ping")
                    temp = "{}{}{}".format(x, y.group(), z2.group())
                    print(temp)
            log.write("temp_pin: {}          temp: {}\n".format(temp_pin, temp))
            return temp
        else:
            return False
        
        
##scan and map logic## 
#1. implicit find (not insert thats later)
#2. explicit find and fill data


for pin in n7_out_data:
    temp = check_signal_mapping_swap(pin["Net Name (ubmp N7 die)"])
    if(temp != False):
        for ballout in c4_data:
            if temp == ballout["ballout_name"] and ballout["ballout_name"] != None:
                    pin["Ballout Number"] = ballout["ballout_number"]
                    pin["Net Name (C4 Bump)"] = ballout["ballout_name"]
                    pin["Net Name (Ballout)"] = ballout["ballout_name"]  
                    pin["X Coord (C4 Bump)"] = None
                    pin["Y Coord (C4 Bump)"] = None
                    if ballout["matched"] == True:
                        
                        print("overwrite attempted (1)" + ballout["ballout_name"])
                        
                        continue
                    ballout["matched"] = True       
    else:
        for ballout in c4_data:
            if( implicit.get( pin["Net Name (ubmp N7 die)"] , 'missing') != 'missing'  ):
                #special case VSS - GD (only once)
                if pin["Net Name (ubmp N7 die)"] == "GD":
                    pin["Net Name (ubmp HBM3 DRAM)"] = "VSS"
                pin["Net Name (C4 Bump)"] = implicit[pin["Net Name (ubmp N7 die)"]]
                pin["Net Name (Ballout)"] = implicit[pin["Net Name (ubmp N7 die)"]]
                pin["Ballout Number"] = "N/A"
                pin["X Coord (C4 Bump)"] = "N/A"
                pin["Y Coord (C4 Bump)"] = "N/A"
                ballout["power"] = True
            elif  pin["Net Name (ubmp N7 die)"] == ballout["ballout_name"] and ballout["ballout_name"] != None:
                    pin["Ballout Number"] = ballout["ballout_number"]
                    pin["Net Name (C4 Bump)"] = ballout["ballout_name"]
                    pin["Net Name (Ballout)"] = ballout["ballout_name"]  
                    pin["X Coord (C4 Bump)"] = None
                    pin["Y Coord (C4 Bump)"] = None
                    if ballout["matched"] == True:
                        
                        print("overwrite attempted (1)" + ballout["ballout_name"])
                        
                        continue
                    ballout["matched"] = True

#2.b now insert those rows from earlier from implicit / power mapping 

##some functions to be used in this process are defined here: 

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

def create_element_hbm(nn_d, nn_b, ballout_num):
    new_dict_element = dict.fromkeys(n7_template,"N/A")
    new_dict_element["Net Name (ubmp N7 die)"] = "N/A"
    ##SPECIAL CASE VSS##
    if nn_b == "VSS":
        new_dict_element["Net Name (ubmp N7 die)"] = "GD"
    new_dict_element["Pin Number"] = "N/A"
    new_dict_element["Net Name (Ballout)"] = nn_b
    new_dict_element["Net Name (C4 Bump)"] = nn_b
    new_dict_element["Ballout Number"] = ballout_num
    new_dict_element["Net Name (ubmp HBM3 DRAM)"]= nn_d
    return new_dict_element

def add_relation_hbm(NN_D, NN_BO, i):
    for ballout in c4_data:
        if NN_BO == ballout["ballout_name"]:
            new_element = create_element_hbm(NN_D, NN_BO, ballout["ballout_number"])
            n7_out_data.insert(i, new_element)
            ballout["matched"] = "x"


def create_element(nn_d, nn_b, ballout_num):
    new_dict_element = dict.fromkeys(n7_template,"N/A")
    new_dict_element["Net Name (ubmp N7 die)"] = nn_d
    new_dict_element["Pin Number"] = "N/A"
    new_dict_element["Net Name (Ballout)"] = nn_b
    new_dict_element["Net Name (C4 Bump)"] = nn_b
    new_dict_element["Ballout Number"] = ballout_num
    new_dict_element["Net Name (ubmp HBM3 DRAM)"]= "N/A"
    ##SPECIAL CASE VSS##
    if nn_b == "VSS":
        new_dict_element["Net Name (ubmp HBM3 DRAM)"]= "VSS"
    return new_dict_element
                        
def add_relation(NN_D, NN_BO, i):
    for ballout in c4_data:
        if NN_BO == ballout["ballout_name"]:
            new_element = create_element(NN_D, NN_BO, ballout["ballout_number"])
            n7_out_data.insert(i, new_element)
            if ballout["matched"] == True:
                
                print("overwrite attempted (2)" + ballout["ballout_name"])
                
                continue
            ballout["matched"] = True


#perform the insertion (2.b)
i = 0
for pin in n7_out_data:
    if( implicit.get( pin["Net Name (ubmp N7 die)"] , 'N/A') != 'N/A'  ):
        add_relation(pin["Net Name (ubmp N7 die)"], implicit[ pin["Net Name (ubmp N7 die)"] ], i)
        implicit.pop(pin["Net Name (ubmp N7 die)"])
    i += 1



##3. map n7-hbm3
for pin in n7_out_data:
    temp = check_signal_mapping_swap(pin["Net Name (ubmp N7 die)"])
    if(temp != False):
        for mem in hbm3_pinsheet_data:
            if temp == mem["Net Name"] and mem["Net Name"] != "VSS":           #the "VSS" should never matter because it will never be in n7, but ill leave here just in case 
                pin["Net Name (ubmp HBM3 DRAM)"] = mem["Net Name"]
                pin["X Coord (HBM3 ubmp)"] = mem["X Coord (design)"]
                pin["Y Coord (HBM3 ubmp)"] = mem["Y Coord (design)"]
                pin["X Coord (C4 Bump)"] = "N/A" 
                pin["Y Coord (C4 Bump)"] = "N/A" 
                mem["Pin Number"] = "x"  
    else:        
        for mem in hbm3_pinsheet_data:
            if pin["Net Name (ubmp N7 die)"] == mem["Net Name"] and mem["Net Name"] != "VSS":           #the "VSS" should never matter because it will never be in n7, but ill leave here just in case 
                pin["Net Name (ubmp HBM3 DRAM)"] = mem["Net Name"]
                pin["X Coord (HBM3 ubmp)"] = mem["X Coord (design)"]
                pin["Y Coord (HBM3 ubmp)"] = mem["Y Coord (design)"]
                pin["X Coord (C4 Bump)"] = "N/A" 
                pin["Y Coord (C4 Bump)"] = "N/A" 
                mem["Pin Number"] = "x"



 #AT THIS POINT N7 - HBM3 AND N7 - BALLOUT IS FILLED OUT



#floating pins
t = len(n7_out_data) #index of end of n7 stuff
for mem in hbm3_pinsheet_data:
    if mem["Pin Number"] != "x":
        pin_number = "N/A"
        net_name_N7 = "N/A"
        net_name_HBM3 = mem["Net Name"]
        net_name_C4 = "N/A"
        net_name_Ballout = "N/A"
        x_N7 = "N/A"
        y_N7 = "N/A"
        x_HBM3 = mem["X Coord (design)"]
        y_HBM3 = mem["Y Coord (design)"]
        x_C4 = "N/A"
        y_C4 = "N/A"
        ballout_number = "N/A"
        make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number)
 
for i in range(t, len(n7_out_data)):
    for ballout in c4_data:
        #implicit powers, label gd but dont insert these rows again (done above)
        if power.get(n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"], "missing") != "missing":
            ##SPECIAL CASE VSS##
            if n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"] == "VSS":
                n7_out_data[i]["Net Name (ubmp N7 die)"] = "GD"
            n7_out_data[i]["X Coord (C4 Bump)"] = "N/A"
            n7_out_data[i]["Y Coord (C4 Bump)"] = "N/A"
            n7_out_data[i]["Net Name (C4 Bump)"] = n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"]
            n7_out_data[i]["Net Name (Ballout)"] = n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"]
            ballout["power"] = True
        elif n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"] == ballout["ballout_name"] and ballout["ballout_name"] != None:
            n7_out_data[i]["X Coord (C4 Bump)"] = None
            n7_out_data[i]["Y Coord (C4 Bump)"] = None
            n7_out_data[i]["Net Name (C4 Bump)"] = n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"]
            n7_out_data[i]["Net Name (Ballout)"] = n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"]
            ballout_number = ballout["ballout_number"]
            n7_out_data[i]["Ballout Number"] = ballout_number
            if ballout["matched"] == True:
                
                print("overwrite attempted (3)" + ballout["ballout_name"])
                
                continue
            ballout["matched"] = True

for i in range(t, len(n7_out_data)):
    if n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"] == "VSS":
        continue
    if power.get(n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"], "missing") != "missing":
        add_relation_hbm(n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"], n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"], i)
        power.pop(n7_out_data[i]["Net Name (ubmp HBM3 DRAM)"])


df = pandas.DataFrame(data=n7_out_data)
df.to_excel("n7_output_xl.xlsx", index=False, freeze_panes=(1,0))
log.close()
for ballout in c4_data:
    if ballout["matched"] == None:
        print("unmatched ballout: {}     {}".format(ballout["ballout_number"], ballout["ballout_name"]))