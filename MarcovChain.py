# Load libraries
from pandas import read_csv
import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np
import random

# Read text file
url = "SW_ALL.txt"
ds = read_csv(url, sep=" ", header=None, names=["Number", "character", "line"])
del ds['Number']

# Create dataset for first dataframe
data1 = {'character': ds["character"],
        'line': ds["line"]}
df = pd.DataFrame(data1)

# Create dataset for second dataframe
data2 = {'character': df['character'].str.replace(' ', ''),
         'line': ds["line"]}
df2 = pd.DataFrame(data2)


# Create dataframe with main characters
toDropTemp = []
for idx, name in enumerate(df2['character'].value_counts().index.tolist()):
    if df2['character'].value_counts()[idx] < 20:
        toDrop = df2[df2["character"] == name].index.values
        toDropTemp.extend(toDrop)
df3 = df2.drop(toDropTemp)


# Move data into a dictionary with each character as a key and their lines as a corresponding string
# Create list of character names each time they have a line
lineDict = {}
charOrder = ""
for index, row in df3.iterrows():
    charOrder = charOrder + " " + df3["character"][index]
    if df3["character"][index] in lineDict:
        lineDict[df3["character"][index]] = lineDict[df3["character"][index]] + " " + df3["line"][index]
    else:
        lineDict[df3["character"][index]] = df3["line"][index]


# Marcov chain function
def Marcov(dict, num):
    corpus = dict.split(" ")

    def make_pairs(corpus):
        for i in range(len(corpus) - 1):
            yield (corpus[i], corpus[i + 1])

    pairs = make_pairs(corpus)

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    first_word = np.random.choice(corpus)
    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]
    n_words = num

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    sample = ' '.join(chain)
    return sample


# Create order of characters
order = Marcov(charOrder, 10).split(" ")

# Create a sample line of text for each character occurs in order
for key in order:
    print(key, Marcov(lineDict.get(key), random.randint(10, 30)))


