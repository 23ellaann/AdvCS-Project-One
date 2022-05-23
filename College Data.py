import pandas
import seaborn as sn
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# DATA SETS
# Complete Dataset
df = pandas.read_csv('MERGED2019_20_PP.csv', index_col='INSTNM')

# Simple Analysis Dataframe
data1 = {'highestDegree': df["HIGHDEG"],
         'adminRate': df["ADM_RATE"],
         'cost': df["COSTT4_A"],
         'facultySalary': df["AVGFACSAL"],
         'SAT25': df["SATMT25"],
         'SAT75': df["SATMT75"],
         'perEngineering': df["PCIP14"]}
df1 = pandas.DataFrame(data1, columns=['highestDegree', 'adminRate', 'cost', 'facultySalary', 'SAT25', 'SAT75',
                                       'perEngineering'])

# Without SAT dataframe
df2 = (df.loc[:, ~df.columns.isin(
    ['SATVRMID', 'SATMTMID', 'SATWRMID', 'SATVR25', 'SATMT25', 'SATWR25', 'ACTCM25', 'ACTEN25', 'ACTMT25', 'ACTWR25',
     'ACTCMMID', 'ACTENMID', 'ACTMTMID', 'ACTWRMID', 'SAT_AVG_ALL', 'SAT_AVG'])])

# College List
collegeListdf = pandas.DataFrame()
collegeList = []


# FUNCTIONS
# Remove redundant pairs from a dataframe
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop


# Get absolute correlations from a dataframe
def get_top_abs_correlations(dataframe, n):
    au_corr = dataframe.corr().unstack().abs().sort_values(ascending=False).drop_duplicates()
    return au_corr[0:n]


# Return shape of dataframe
def get_shape(dataframe):
    return (dataframe.shape)


# Return correlation of a dataframe (takes a while for large data sets)
def get_correlation(dataframe):
    corr = get_top_abs_correlations(dataframe, 5)
    sn.heatmap(corr, annot=True)
    plt.show()
    return (corr)


def make_SchoolDataFrame(dataframe, value, dropNa):
    newdf = dataframe.loc[value]
    if (dropNa == True):
        newdf = pandas.DataFrame(newdf.dropna())
    return (newdf)

def get_School():
    value = input("Enter the name of the college to add to the list:\n")
    return(value)

def get_dataFrame():
    value = input("Options for data:\n 0: Original data \n 1: Quick summary \n 2: Without test scores \n 3: College dataset")
    if(value == 0):
        return(df)
    elif(value == 1):
        return(df1)
    elif(value == 2):
        return(df2)
    elif(value == 3):
        return(collegeListdf)

def add_schooltoList(value):
    global collegeList
    collegeList.append(value)
    update_schoolListdf(value)

def initiate_schoolListdf():
    global collegeListdf
    value = get_School()
    collegeList.append(value)
    collegeListdf = make_SchoolDataFrame(df, value, False)

def update_schoolListdf(value):
    global df
    global collegeListdf
    frames = [make_SchoolDataFrame(df, value, False), collegeListdf]
    collegeListdf = pandas.concat(frames, axis=1)
    return (collegeListdf)

def print_schoolList():
    print(collegeList)
    print(collegeListdf)

def compare_value(value, dataframe):
    newdf = pandas.DataFrame
    dataframe = dataframe[pandas.to_numeric(dataframe['id'], errors='coerce').notnull()]
    maxValues = dataframe.max(axis=1)
    maxValuesID = dataframe.idxmax(axis = 1)
    print(maxValues)
    print(maxValuesID)

# def interact_withUser():
#         value = input("Options:\n 0: Find shape \n 1: Find correlation \n 2: Create a school list \n 3: Add to school list \n 4: Print school list\n")
#         if (value == "0"):
#             print(get_shape(get_dataFrame()))
#         if(value == 1):
#             get_correlation(get_dataFrame())
#         if(value == 2):
#             initiate_schoolListdf()
#         if(value == 3):
#             add_schooltoList(get_School())
#         if(value == 4):
#             print_schoolList()


#interact_withUser()
