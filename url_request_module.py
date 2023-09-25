import requests

r=requests.get("https://api.github.com/users/Connor-SM")
#print(r)
#print( type(r))

#data=r.content
#print(data)

data=r.json()
for k,v in data.items():
    print("Key:{} \t value:{}".format(k,v))

print(data["name"])