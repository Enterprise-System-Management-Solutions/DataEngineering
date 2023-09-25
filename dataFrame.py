import pandas as pd
import random

##creating a data frame using the from_dist method
#random.seed(3)
names=["Safiyya","Tasdik","Ayan","Ariya","khairul","Hasan"]
ages=[random.randint(2,13) for x in range(len(names))]
people={"Name": names, "Age": ages}
df= pd.DataFrame.from_dict(people)

#print(df)
""" Not worked
columns1=df.columns.values.tolist()
print( columns1[1])
#print( df["names"][2] )

"""
print("-------------------------")
print(df.loc[0])
print("-------------------------")
print(df.loc[2].Name)
print("-------------------------")
#print(df.loc[0]["names"])
print("-------------------------")
print(df[1:3])

print("--------head -----------------")
print(df.head(2))
print("-------- tail-----------------")
print(df.tail(2))

print("-------- column names print-----------------")
headers = df.keys()
print(headers)
print("-------- number of record & colums  of a data frame -----------------")
print(df.shape)
print("-------- data frame sorting -----------------")
#sort_values()
df = df.sort_values(df.columns[1])
print(df.head(4))

print("-------- subsetting data frame -----------------")
df[df.columns[1]>4]
print(df)