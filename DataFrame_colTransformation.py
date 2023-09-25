import pandas as pd
import random

##creating a data frame using the from_dist method
names=["Safiyya","Tasdik","Ayan","Ariya","khairul","Hasan"]
ages=[random.randint(2,13) for x in range(len(names))]
people={"Name": names, "Age": ages}
df= pd.DataFrame.from_dict(people)
#add a new column in data frame
tenure=[random.randint(0,10) for x in range(len(df))]
df["tenure"]=tenure
#print(df.head())
""" use apply method to catagory a group of people"""

def ageGroup(age):
    return "Baby" if age < 7 else "boy"

df["age_group"]=df["Age"].apply(ageGroup)

print("-----------Original Table-------------")
print(df.head())


print("-----------Group By on single  column Table-----------")
print(df.groupby("age_group", as_index=False).count().head())

print("-----------Group By on mutipole column Table-----------")
print(df.groupby(["age_group","tenure"], as_index=False).count().head())

print("-----------add a new record-----------")
print(df.head())
df.loc[5]=["Safin",11,5,"boy"]
df.loc[6]=["Safin",12,5,"boy"]
print(df)

print("-----------Drop duplicate-----------")
df=df.drop_duplicates(subset="Name")
print(df)

