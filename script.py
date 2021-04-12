from ytmusicapi import YTMusic
import csv
import time

ytmusic = YTMusic('./src/headers_auth.json')
playlists = ytmusic.get_library_playlists()
lib_playlists = {}
playlist_ids = []

for i in playlists:
    playlist_ids.append(i['playlistId'])
    lib_playlists[i['title']] = i

# print(playlist_ids)
playlist = ytmusic.get_playlist(playlist_ids[2])
# print(playlist)

new_playlist = ytmusic.create_playlist('Imported Songs','Youtube API Test!!')

filename = "songs.csv"
rows = []
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row[0])

failed = []
file = open("failed_songs.txt","w")
count = 0


for i in rows:
    count+=1
    print(count)
    # time.sleep(0.5)
    # print("sleeping")
    song_result = ytmusic.search(i,'songs')

    # print(len(song_result))
    if len(song_result) > 0:
        if i != song_result[0]['title']:
            video_result = ytmusic.search(i,'videos')
            if len(video_result) > 0:
                # print(video_result[0]['videoId'])
                ytmusic.add_playlist_items(new_playlist,[video_result[0]['videoId']])
            else:
                print("Failed Plus ONEEEEE")
                file.write(i + ' \n')
        else:
            # print(song_result[0]['videoId'])
            ytmusic.add_playlist_items(new_playlist,[song_result[0]['videoId']])
    else:
        print("Failed Plus ONEEEEE")
        file.write(i + ' \n')

file.close()
