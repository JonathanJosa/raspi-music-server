import youtube_dl
import requests
import json
import datetime

def insert_json(data_song):
    data = json.load(open("database.json", "r"))
    lon = 1

    timestamp = data_song.get('upload_date')
    if timestamp == None:
        timestamp = "202206"+str(datetime.datetime.now().day)

    data[data_song['title']] = {
        "song": data_song.get('track'),
        "album": data_song.get('album'),
        "artist": data_song.get('artist'),
        "duration": data_song.get('duration'),
        "date": {
            "year": timestamp[0:4],
            "month": timestamp[4:6],
            "day": timestamp[6:8]
        },
        "song_number": lon
    }

    json.dump(data, open("database.json", "w"))
    print("Saved on database, saves: "+str(lon))

    return lon


def download_song(url_video, id):

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f"data/music/{id}",
        'writethumbnail': True,
        'quiet': True
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        print("Downloading")
        ydl.download([url_video])
    print("Process completed")


def busqueda(search, keep=False):
    res = requests.get("https://www.youtube.com/results?search_query="+search.replace(" ", "+"))
    extraction = res.text
    while(keep):
        fs = extraction.find("/watch?v=")
        query = extraction[fs: fs+(extraction[fs: fs+40]).find('"')]
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = "https://www.youtube.com"+query,
            download = False,
            extra_info = {'quiet': True}
        )
        print(video_info.keys())
        print("Song: "+video_info['title'])
        if video_info['artist'] != None:
            print("  From: "+video_info['artist'])
        if keep:
            ans = input("\nDownload(y/n)? ")
            if ans == "Y" or ans == "" or ans == "y":
                break
            else:
                extraction = extraction[fs::]

    download_song(video_info['webpage_url'], insert_json(video_info))


if __name__ == "__main__":
    busqueda(input("Busqueda: "), True)
