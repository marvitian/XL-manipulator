import re


list0 = [
    "ATSTc",
    "ATSTd",
    "ATSTg"
]
# CKd_c
# text = "ATSTd"

# for i in list0: 
#     # print(i)
#     # x = re.search("ATST[A-Z]", i)
#     x = re.search("{}[cg]".format(text), i)
#     if(x != None):
#         print(x.group())


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

text = "CKd_c"


# text will act as the  pin["Net Name (ubmp N7 die)"] 
x = re.search("\A[A-Z]+", text)
y = re.search("[a-z]", text)
z1 = re.search("[0-9]+", text)
z2 = re.search("[0-9]*[_][ct]?", text)
if x != None:
    if(list1.get(x.group(), 'missing') != 'missing'):
        print('success')
        if(letter_match.get(y.group(), 'missing') != 'missing'):
            print("new mapping")
            temp = "{}{}".format(x.group(),letter_match[y.group()])
            print(temp)
        else:
            print("not new mapping")
            temp = "{}{}".format(x.group(), y.group())



    elif(list2.get(x.group(), 'missing') != 'missing'):
        print('success 2')
        if(letter_match.get(y.group(), 'missing') != 'missing'):
            print("new mapping")
            temp = "{}{}{}".format(x.group(), letter_match[y.group()], z1.group())
            print(temp)
        else:
            print("not new mapping")
            temp = "{}{}{}".format(x.group(), y.group(), z1.group())
            print(temp)



    elif(list3.get(x.group(), 'missing') != 'missing'):
        print('success 2')
        if(letter_match.get(y.group(), 'missing') != 'missing'):
            print("new mapping")
            temp = "{}{}{}".format(x.group(), letter_match[y.group()], z2.group())
            print(temp)
        else:
            print("not new mapping")
            temp = "{}{}{}".format(x.group(), y.group(), z2.group())
            print(temp)


