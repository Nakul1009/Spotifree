import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *
from pytube import YouTube
import os

from flask import Flask,request,render_template
app = Flask(__name__, template_folder='Frontend', static_folder='static')


@app.route('/')
def index():
    return render_template('indexx.html')

@app.route('/submit',methods=['POST'])
def submit_form():
    
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
            return None


    def video_search(songname):
        try:
            search = VideosSearch(songname, limit=1)
            a = search.result()
            tempo = a["result"][0]
            songlink = tempo["link"]
            return songlink
        except:
            return None



    def song_download(yt, downloadpath):
        try:
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=downloadpath)
            # the extension of the file is converted into mp3
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            return True,"Successfully mp3 file downloaded"
            # if mp3 does not exist mp4 is downloaded
        except:
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
                return False,"Sorry no file exist"

            return True , "Successfully mp4 file downloaded"


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
        return True


    """Finishing of the used Functions"""


    # getting input from the user for the song name
    spotify_link = request.form.get('spotifyLink')
    try:
        req = requests.get(spotify_link)
    except:
        return render_template('Output.html', message="Enter a valid link")

    # getting the type of link (track, playlist, album)
    type_name = spotify_link.split("/")

    # default download path
    downloadpath = os.path.join(os.environ["USERPROFILE"], "Downloads")

    if "open.spotify.com" in type_name:

        if "track" in type_name:
            # finding the song name
            song_name = find_song_name(req)
            if song_name:
                # searching for the song in youtube
                songlink = video_search(song_name)
                if songlink:
                    # downloading the video
                    yt = YouTube(songlink)
                    success , message = song_download(yt, downloadpath)
                    if success:
                        return render_template('Output.html', song_name=song_name, message = message)
                    else:
                        return render_template('Output.html', song_name=song_name, message = message)
                else:
                    return render_template('Output.html', song_name=song_name, message = "link not found")
            else:
                return render_template('Output.html',  message = "song not found")


        elif "album" in type_name:
            # finding album name
            album_name = find_song_name(req)
            if album_name:
                # creating a folder with the album name for the songs to get downloaded in it
                album_playlist_downloader(album_name)
                return render_template('Output.html',  message = "successfully album downloaded",album_name = album_name)
            else:
                return render_template('Output.html',  message = "playlist not found")

        elif "playlist" in type_name:
            # finding playlist name
            playlist_name = find_song_name(req)
            if playlist_name:
                # creating a folder with the album name for the songs to get downloaded in it
                album_playlist_downloader(playlist_name)
                return render_template('Output.html',  message = "successfully album downloaded",playlist_name = playlist_name)
            else:
                return render_template('Output.html',  message = "playlist not found")

        else:
            return render_template('Output.html',  message = "The given link is not of a track or a playlist or a album please check the link you have given!!!")

    else:
        return render_template('Output.html',  message =  "The given link is not of spotify please check the link you have given!!!")
    
if __name__ == '__main__':
    app.run(debug=True)    




