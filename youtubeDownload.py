import youtube_dl
import requests
import json
import datetime

def insert_json(data_song):
    data = json.load(open("database.json", "r"))
    lon = len(data["songs"])
    if lon > 0:
        last = data["songs"][-1]["song_number"] + 1
    else:
        last = 1

    timestamp = data_song.get('upload_date')
    if timestamp == None:
        timestamp = "202206"+str(datetime.datetime.now().day)

    data["songs"].append({
        "title": data_song.get('title') or "Unknow",
        "song": data_song.get('track') or "Unknow",
        "album": data_song.get('album') or "Unknow",
        "artist": data_song.get('artist') or "Unknow",
        "duration": data_song.get('duration') or 1,
        "date": {
            "year": timestamp[0:4],
            "month": timestamp[4:6],
            "day": timestamp[6:8]
        },
        "song_number": last
    })

    json.dump(data, open("database.json", "w"))

    return last


def download_song(url_video, id):

    yield("Downloaded song_id: "+str(id))
    options = {
        'skip_download': True,
        'outtmpl': f"data/music/{id}_thumbnail",
        'writethumbnail': True,
        'quiet': True
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        yield("Downloading Thumbnail")
        ydl.download([url_video])

    options = {
        'format': 'bestaudio/best',
        'outtmpl': f"data/music/{id}.mp3",
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': True
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        yield("Pirateando cancion")
        ydl.download([url_video])
    yield("Cancion pirateada")

def busqueda(search, keep=False):
    res = requests.get("https://www.youtube.com/results?search_query="+search.replace(" ", "+"))
    extraction = res.text
    while(True):
        fs = extraction.find("/watch?v=")
        query = extraction[fs: fs+(extraction[fs: fs+40]).find('"')]
        video_info = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            url = "https://www.youtube.com/"+query,
            download = False
        )

        yield("Song: "+video_info['title'])
        if video_info.get('artist') != None:
            yield("  From: "+video_info['artist'])
        if keep:
            ans = input("\nDownload(y/n)? ")
            if ans == "Y" or ans == "" or ans == "y":
                break
            else:
                extraction = extraction[fs+40::]
        else:
            break

    for msg in download_song(video_info['webpage_url'], insert_json(video_info)):
        yield msg


if __name__ == "__main__":
    for msg in busqueda(input("Busqueda: "), True):
        print(msg)
