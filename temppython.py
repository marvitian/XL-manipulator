def make_cell(pin_number, net_name_N7, net_name_HBM3, net_name_C4, net_name_Ballout, x_N7, y_N7, x_HBM3, y_HBM3, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(template_data,"N/A") #create new dictionary from template (template_data is the json.load(file) of template.json)
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
    new_dict_element["y  Coord (C4 Bump)"] = y_C4
    new_dict_element[name_balloout_number] = ballout_number





def n7_ball_match(pin_number, net_name_N7, net_name_C4, net_name_Ballout, x_N7, y_N7, x_C4, y_C4, ballout_number):
    new_dict_element = dict.fromkeys(template_data,"N/A") #create new dictionary from template (template_data is the json.load(file) of template.json)
    new_dict_element["Pin Number"] = pin_number
    new_dict_element["Net Name (ubmp N7 die)"] = net_name_N7
    new_dict_element["Net Name (C4 Bump)"] = net_name_C4
    new_dict_element["Net Name (Ballout)"] = net_name_Ballout
    new_dict_element["X Coord (N7 ubmp)"] = x_N7
    new_dict_element["Y Coord (N7 ubmp)"] = y_N7
    new_dict_element["X Coord (C4 Bump)"] = x_C4
    new_dict_element["y  Coord (C4 Bump)"] = y_C4
    new_dict_element[name_balloout_number] = ballout_number
    return new_dict_element


    pin_number = pin["Pin Number"]
    net_name_N7 = pin[name_net_name_die]
    net_name_C4 = pin[name_net_name_bumb]
    net_name_Ballout = pin[name_net_name_ballout]
    x_N7 = pin["X Coord (N7 ubmp)"]
    y_N7 = pin["Y Coord (N7 ubmp)"]
    x_C4 = pin["X  Coord (C4 Bump)"]
    y_C4 = pin["Y  Coord (C4 Bump)"]
    ballout_number = ballout_number


    def n7_hbm3_match(pin_number, net_name_N7, net_name_HBM3, x_N7, y_N7, x_HBM3, y_HBM3, ballout_number)