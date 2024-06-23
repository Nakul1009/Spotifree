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


playinp = input("enter the playlist link")
playpri = requests.get(playinp)
playinp = playinp.split("/")

if "playlist" in playinp:

    playsong = BeautifulSoup(playpri.content, "html.parser")

    # Playlist name finder
    playlist_name = playsong.find("title")
    playlist_name = str(playlist_name)[7:]
    playlist_name = playlist_name.split("<")
    playlist_name = "".join(playlist_name)

    # to remove the spotify name from the song name
    temp_play = playlist_name.split()
    temp_store_play = temp_play.index("|")
    temp_play = temp_play[0:temp_store_play]
    playlist_name = " ".join(temp_play)

    print(playlist_name)

    metatag = playsong.find_all("meta", attrs={"name": "music:song"})
    playlist = []
    for tag in metatag:
        temp = str(tag)[15:]
        temp1 = temp.split('"')
        playlist.append(temp1[0])

    newpath = downloadpath + "\\" + playlist_name
    flag = False
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        flag = True
        newpath = newpath + "\\"

    for i in playlist:
        pri = requests.get(i)

        # getting the song name from the html get page
        songname = find_song_name(pri)
        print(songname)

        # searching for the song in youtube
        songlink = video_search(songname)
        # downloading the video
        yt = YouTube(songlink)

        # donwloading the songs
        if flag == True:
            # audio only file is saved
            song_download(yt)

elif "album" in playinp:
    pass
