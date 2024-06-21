import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *
from pytube import YouTube
import os





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

#creating a download path for downloading in download folder
downloadpath=os.path.join(os.environ['USERPROFILE'],'Downloads')

#audio only file is saved
try:
    stream = yt.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path=downloadpath)
  
# the extension of the file is converted into mp3 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 

#if mp3 does not exist mp4 is downloaded
except:
    print("Sorry mp3 cannot be found")
    checker = yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(22)
    if checker == None:
        yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(18).download(output_path=downloadpath)
    elif yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(22) != None :
        yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(22).download(output_path=downloadpath)
    else:
        print("Sorry No File Exists")

    print("Mp4 file is downloaded")

    

  