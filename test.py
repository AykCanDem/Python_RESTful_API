import requests

BASE = "http://localhost:5000/"

# Put couple of videos.
data = [
    {'name': "Sagopa Kajmer-Baytar", 'views': 100000, 'likes': 101},
    {'name': "Ceza-Holocaust", 'views': 240000, 'likes': 182},
    {'name': "Ceza-Medcezir", 'views': 135600, 'likes': 533}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i) , data[i])
    print(response.json())

input()
# Put a video that is already posted. (to show the error handling)
response = requests.put(BASE + "video/1" , {'name': "Sagopa Kajmer-Baytar", 'views': 100000, 'likes': 101})
print(response.json())



input()
#Query one of existing video with GET request.
response = requests.get(BASE + 'video/1')
print(response.json())

input()
# update the existing video
response = requests.patch(BASE + 'video/1', {'name': 'Sagopa ve Ceza - Neyim Var ki', 'views': 992134321})
print(response.json())


input()
#delete 
response = requests.delete(BASE + "video/1")
print(response)
