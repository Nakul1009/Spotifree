import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *
from pytube import YouTube


#getting input from the user for the song name
inp = input("enter the link you want to convert into mp4: ")
pri = requests.get(inp)

#getting the song name from the html get page
song = BeautifulSoup(pri.content, "html.parser")
songfind = song.find("title")

#removing the title since it has 7 characters
songfind = str(songfind)[7:]
songfind = songfind.split("<")
songfind = "".join(songfind)

#to remove the spotify name from the song name
temp = songfind.split()
temp_store = temp.index("|")
temp = temp[0:temp_store]
songname = " ".join(temp)

print("Song Name", songname) 

#searching for the song in youtube
search = VideosSearch(songname, limit = 1)
a = search.result()
tempo = a['result'][0]

songlink = tempo['link']




#downloading the video
yt = YouTube(songlink)


yt.streams.filter(only_audio="True").first().download()




















#https://open.spotify.com/track/1JVfJe7LQSePY6EyF1fBUX?si=0fd15bc439de4dde
