import csv
import sqlite3
from matplotlib import pyplot as plt


filename = 'NCHS_-_Leading_Causes_of_Death__United_States.csv'
def csv_to_list(filename):
    csv_list = []
    with open(filename) as f:
        reader = csv.reader(f)
        for line in reader:
            csv_list.append(line)
    return csv_list
csv_list = csv_to_list(filename)

def get_labels(csv_list):
    """ Assigns column titles to header """
    header = csv_list.pop(0)
    return header

header = get_labels(csv_list)

#sqlite3
conn = sqlite3.connect(':memory:')

#Create cursor that allows sql commands
c = conn.cursor()
#creating table
c.execute(""" CREATE TABLE death (
               year INTEGER,
               cause TEXT,
               state TEXT,
               death INTEGER
                ) """)
        
def insert_table(list):
    with conn:
        c.execute("INSERT INTO death VALUES (:year, :cause, :state, :death)", 
                  {'year': list[0], 'cause': list[2], 'state': list[3], 'death': list[4],})
    
def list_to_table(csv_list):
    """ Insert without column names"""
    #print("This is how long this list is: "+ str(len(csv_list)))
    for list in csv_list:
        insert_table(list)
    
def selects_for_line_plot(set_condition_1, list_condition):
    """ list condition will equal the causes """
    """ will need a list of causes and set_condition = a state """
    with conn:
        line_plot = []
        for causes in list_condition:
            for cause in causes:
                c.execute("SELECT year, SUM(death), cause FROM death WHERE cause = :cause AND state = :state GROUP BY year;",
                          {'cause': cause, 'state':set_condition_1})
                line_plot.append(c.fetchall())
    return line_plot 

def x_value(queried_list):
    x_values = []
    for set in queried_list:
        x_values.append(set[0])
    return x_values

def y_value(queried_list):
    y_values = []
    for set in queried_list:
        y_values.append(set[1])
    return y_values

def line_graph_ready_express(selects_for_list):
    """ must be used after selects_for_line_plot function, enter its return for as an argument"""
    ultimate_list = []
    holder_list = []
    x_value = []
    y_value = []
    for results in selects_for_list:
        for result in results:
            x_value.append(result[0])
            y_value.append(result[1])
    #x_value=([i for i in holder_list if holder_list.index(i)%2==0])
    #y_value=([i for i in holder_list if holder_list.index(i)%2!=0])
    ultimate_list.append(x_value)
    ultimate_list.append(y_value)
    holder_list.clear()
    for results in selects_for_list:#access three big lists
        for result in results:
            if result[2] not in holder_list:
                holder_list.append(result[2])
    ultimate_list.append(holder_list)
    return ultimate_list

#ENTERING ALL THE DATA IN DB
list_to_table(csv_list)
c.execute("DELETE FROM  death WHERE state ='United States' OR state = 'District of Columbia' OR cause = 'All causes';")
conn.commit()

#creating variables
c.execute("SELECT DISTINCT(cause) FROM death;")
causes_list = (c.fetchall())

line = selects_for_line_plot("California", causes_list)
ultimate_list = line_graph_ready_express(line)

new_york = selects_for_line_plot("New York", causes_list)
new_york_list = line_graph_ready_express(new_york)

texas = selects_for_line_plot("Texas", causes_list)
texas_list = line_graph_ready_express(texas)

conn.close()


def x_axis_final(list):
    """ x_axis must be equal to  [0]""" 
    x = list[0]
    num = 18
    x_axis = [[i for i in x[num*i:num*i+18]] for i in range(int(len(x)/18))]
    return x_axis

def y_axis_final(list):
    """ x_axis must be equal to  [1]""" 
    y = list[1]
    num = 18
    y_axis = [[i for i in y[num*i:num*i+18]] for i in range(int(len(y)/18))]
    return y_axis


x_axis = x_axis_final(ultimate_list)
y_axis = y_axis_final(ultimate_list)
for i in range(10):
    plt.plot(x_axis[i], y_axis[i])
plt.legend(ultimate_list[2], loc='best')
plt.title("Deaths in California")
plt.xticks(x_axis[0])
plt.show()

new_x = x_axis_final(new_york_list)
new_y = y_axis_final(new_york_list)
for i in range(10):
    plt.plot(new_x[i], new_y[i])
plt.legend(ultimate_list[2], loc='best')
plt.title("Deaths in New York")
plt.xticks(x_axis[0])
plt.show()

new_x = x_axis_final(texas_list)
new_y = y_axis_final(texas_list)
for i in range(10):
    plt.plot(new_x[i], new_y[i])
plt.legend(ultimate_list[2], loc='best')
plt.title("Deaths in Texas")
plt.xticks(x_axis[0])
plt.show()