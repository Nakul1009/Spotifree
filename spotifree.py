import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *
from pytube import YouTube
import os
import sys

"""Every required Functions"""


def find_song_name(pri):
    try:
        songb = BeautifulSoup(pri.content, "html.parser")
        songfind = songb.find("title")
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
    except:
        print()
        print("-------------------------")
        print("Please check your link")
        print("-------------------------")
        sys.exit()


def video_search(songname):
    try:
        search = VideosSearch(songname, limit=1)
        a = search.result()
        tempo = a["result"][0]
        songlink = tempo["link"]
        return songlink
    except:
        print()
        print("-------------------------")
        print("Please check your link")
        print("-------------------------")
        sys.exit()



def song_download(yt, downloadpath):
    try:
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=downloadpath)
        # the extension of the file is converted into mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        print()
        print("-----------------------")
        print("Successfully downloaded")
        print("-----------------------")
        # if mp3 does not exist mp4 is downloaded
    except:
        print()
        print("-------------------------")
        print("Sorry mp3 cannot be found")
        print("-------------------------")
        checker = yt.streams.filter(
            progressive="True", file_extension="mp4"
        ).get_by_itag(22)
        if checker == None:
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(
                18
            ).download(output_path=downloadpath)
        elif (
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(22)
            != None
        ):
            yt.streams.filter(progressive="True", file_extension="mp4").get_by_itag(
                22
            ).download(output_path=downloadpath)
        else:
            print()
            print("--------------------")
            print("Sorry No File Exists")
            print("--------------------")

        print()
        print("----------------------")
        print("Mp4 file is downloaded")
        print("----------------------")


def album_playlist_downloader(name):
    song = BeautifulSoup(req.content, "html.parser")
    metatag = song.find_all("meta", attrs={"name": "music:song"})
    playlist = []
    for tag in metatag:
        temp = str(tag)[15:]
        temp1 = temp.split('"')
        playlist.append(temp1[0])

    newpath = downloadpath + "\\" + name
    flag = False
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        flag = True
        newpath = newpath + "\\"

    for i in playlist:
        pri = requests.get(i)

        # getting the song name from the html get page
        songname = find_song_name(pri)
        print()
        print(songname)

        # searching for the song in youtube
        songlink = video_search(songname)
        # downloading the video
        yt = YouTube(songlink)

        # donwloading the songs
        if flag == True:
            # audio only file is saved
            song_download(yt, newpath)


"""Finishing of the used Functions"""


# getting input from the user for the song name
inp = input("enter the link you want to convert into mp3: ")
try:
    req = requests.get(inp)
except:
    print()
    print("-----------------")
    print("enter a valid url")
    print("-----------------")
    sys.exit()

# getting the type of link (track, playlist, album)
type_name = inp.split("/")

# default download path
downloadpath = os.path.join(os.environ["USERPROFILE"], "Downloads")

if "open.spotify.com" in type_name:

    if "track" in type_name:
        # finding the song name
        song_name = find_song_name(req)

        # printing the song name
        print(song_name)

        # searching for the song in youtube
        songlink = video_search(song_name)

        # downloading the video
        yt = YouTube(songlink)
        song_download(yt, downloadpath)

    elif "album" in type_name:
        # finding album name
        album_name = find_song_name(req)

        # printing album name
        print(album_name)

        # creating a folder with the album name for the songs to get downloaded in it
        album_playlist_downloader(album_name)

    elif "playlist" in type_name:
        # finding playlist name
        playlist_name = find_song_name(req)

        # printing album name
        print(playlist_name)

        # creating a folder with the album name for the songs to get downloaded in it
        album_playlist_downloader(playlist_name)

    else:
        print()
        print(
            "-------------------------------------------------------------------------------------------------"
        )
        print(
            "The given link is not of a track or a playlist or a album please check the link you have given!!!"
        )
        print(
            "-------------------------------------------------------------------------------------------------"
        )

else:
    print()
    print("------------------------------------------------------------------------")
    print("The given link is not of spotify please check the link you have given!!!")
    print("------------------------------------------------------------------------")
