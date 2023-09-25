"""
There is two data frames
1st example based on inner join and 2nd one is the outer join
"""

import pandas as pd
import random

##creating a data frame using the from_dist method
#random.seed(3)
names=["Safiyya","Tasdik","Ayan","Ariya","khairul","Hasan"]
ages=[random.randint(2,13) for x in range(len(names))]
people={"names": names, "Age": ages}
df= pd.DataFrame.from_dict(people)
print("------1st Table")
print(df)

ratings={ "names" :["Tasdik","Ayan"], "ratings":[10,3]}
ratings=df.from_dict(ratings)
print("------2nd Table")
print(ratings)

print("------Inner Join")
matched_ratings=df.merge(ratings, on="names", how="inner")
print(matched_ratings.head())

print("------Outer Join")

all_ratings=df.merge(ratings, on="names", how="outer")
print(all_ratings.head())