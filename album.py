import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *
from pytube import YouTube
import os


def find_song_name(pri):
    song = BeautifulSoup(pri.content, "html.parser")
    songfind = song.find("title")
    # removing the title since it has 7 characters
    songfind = str(songfind)[7:]
    songfind = songfind.split("<")
    songfind = "".join(songfind)

    # to remove the spotify name from the song name
    temp = songfind.split()
    temp_store = temp.index("|")
    temp = temp[0:temp_store]
    songname = " ".join(temp)
    return songname


def song_download(yt):
    try:
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=newpath)
        # the extension of the file is converted into mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        # if mp3 does not exist mp4 is downloaded
    except:
        print("Sorry mp3 cannot be found")
        checker = yt.streams.filter(
            progressive="True", file_extension="mp4"
        ).get_by_itag(22)
        if checker == None:
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(
                18
            ).download(output_path=newpath)
        elif (
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(22)
            != None
        ):
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(
                22
            ).download(output_path=newpath)
        else:
            print("Sorry No File Exists")

        print("Mp4 file is downloaded")




def video_search(songname):
    search = VideosSearch(songname, limit=1)
    a = search.result()
    tempo = a["result"][0]
    songlink = tempo["link"]
    return songlink


# creating a download path for downloading in download folder
downloadpath = os.path.join(os.environ["USERPROFILE"], "Downloads")


albinp = input("enter the albun link")
albpri = requests.get(albinp)
albinp = albinp.split("/")


song = BeautifulSoup(albpri.content, "html.parser")
album_name = song.find("title")
album_name = str(album_name)[7:]
album_name = album_name.split("<")
album_name = "".join(album_name)

    # to remove the spotify name from the song name
temp_play = album_name.split()
temp_store_play = temp_play.index("|")
temp_play = temp_play[0:temp_store_play]
album_name = " ".join(temp_play)

print(album_name)
meta=song.find_all("meta",attrs={"name":"music:song"})
newpath = downloadpath + "\\" + album_name
flag = False
if not os.path.exists(newpath):
    os.makedirs(newpath)
    flag = True
    newpath = newpath + "\\"

for i in meta:
    temp=str(i)[15:]
    temp1=temp.split("\"")
    pri=requests.get(temp1[0])

    songname=find_song_name(pri)
    print(songname)
    songlink=video_search(songname)
    yt=YouTube(songlink)
    if flag:
        song_download(yt)

