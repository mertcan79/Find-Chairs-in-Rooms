####### THE PROGRAM FINDS THE FIRST AND LAST PLUS SIGNS ON THE LEFT AND RIGHT SIGNS OF 
####### THE NAME OF THE ROOM AND EXTRACTS THE DATA BETWEEN IT. THEN IT COUNTS THE CHAIRS INSIDE THE EXTRACTED STRINGS

###### AUTHOR:MERTCAN COSKUN

import re
import numpy as np

#OPEN THE FILE AND REAL LINES. APPEND TO AN ARRAY
list_of_lists = []
with open('rooms.txt') as f:
    for line in f:
        list_of_lists.append([elt.strip() for elt in line.split(',')])

#FIND MAX LENGTH OF LINES
max_len = 0
for i in list_of_lists:
    if len(i[0])>max_len:
        max_len = len(i[0])

#APPEND BLANKS IN THE BEGGINING IF LINES ARE SHORTER THAN OTHERS
new_array = []
for i in list_of_lists:
    i = ' '*(max_len-len(i[0])) + i[0]
    new_array.append(i)

#MAIN FUNCTION TO COUNT ROOMS
def calculate_rooms(find):
    full_res = []
    #IF TOTAL, USE FULL ARRAY
    if find == "total":
        full_res = new_array
    else:

        #FUNCTION TO FIND ALL THE "+"
        def find_fun(str, ch):
            for i, ltr in enumerate(str):
                if ltr == ch:
                    yield i

        #START OF ROOM INDEXES        
        for count, i in enumerate(new_array):
            if find in i:
                start_v = count
                start_h = i.find(find)

        #START OF PLUS INDEXES      
        for count, i in enumerate(new_array[:start_v]):
            if '+' in i and i.find('+') < start_h:
                start_v_plus = count
                c = list(find_fun(i, "+"))
                #CHOOSE THE CLOSEST PLUS SIGN
                start_h_plus=min(enumerate(c), key=lambda x: abs(start_h - x[1]))[1]

        #END OF PLUS INDEXES
        for count, i in enumerate(new_array[start_v:]):
            #CHECK IF ANY OF THE PLUS INDEXES IS GREATER THAN STARTING POINT
            a = any(y > start_h for y in list(find_fun(i, "+")))
            if '+' in i and a:
                end_v_plus = count + start_v
                end_h_plus = i[start_h+len(find)+2:].find('+') + start_h+len(find)+2
                break

        #IF NUMBER OF ROWS IS GREATER THAN THE INDEX OF THE PLUS SIGN, EXTRACT THE ROWS BETWEEN FIRST AND LAST PLUS 
        for count, i in enumerate(new_array):
            if start_v_plus < count:
                full_res.append(i[start_h_plus:end_h_plus])
            #IF LAST ROW IS REACHED, STOP
            if count == end_v_plus:
                break

    #INITIATE DICTIONARY
    dict_res = {"P":0,"W":0,"S":0,"C":0}

    for i in full_res:
        #ADD CHAIRS
        dict_res["P"] = dict_res.get("P", 0) + i.count("P")
        
        dict_res["S"] = dict_res.get("S", 0) + i.count("S")
        
        dict_res["W"] = dict_res.get("W", 0) + i.count("W")
        
        dict_res["C"] = dict_res.get("C", 0) + i.count("C")
    return dict_res

#FIND ALL THE ROOMS IN THE PLAN
rooms = []
results = {}
for i in new_array:
    room_ = re.findall('\(.*?\)',i)
    if len(room_)>0:
        rooms.append(room_)

flat_list = [item for sublist in rooms for item in sublist] 
#SORT BY NAME
flat_list.sort()
#INSERT TOTAL IN THE BEGINNING
flat_list.insert(0,"total")

for i in flat_list:
    #REPLACE PARANTHESES WITH BLANK
    i=i.replace( "(", "" ).replace(")", "" )
    #ASSIGN ROOM TO FUNCTION
    func_res = calculate_rooms(i)
    results[i] = func_res
    #PRINT THE ROOM AND THE CHAIRS
    print(i, ":","\n", results[i])
