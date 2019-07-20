from flask import Flask, request, jsonify, json
import requests

api = Flask(__name__)

@api.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the FastTracks Microservice!</h1>"

@api.route('/api/v1/recommended', methods=['GET'])
def parse_request():
    data = request.form
    ids = data['song_ids']
    return get_recommended_songs(ids)

def get_recommended_songs(ids):
    params = {'seed_tracks': ids, 'limit': 10}
    headers = {'Authorization': 'Bearer BQDPH3xjcCRoSZEleJtDrsOq6X21UHm6fQ8wKN_2UjSPFGSigWq3-QBDlSSNMizwpy5zElyeModIMty0xGzYuRoA-397MM5pL3_3pQVkTIt1NG3-RIH1nRz6yN3_IeHRMiHedkWgy7Pbo7naiCjxlgs0GFYVGjtvyQ'}
    songs = requests.get('https://api.spotify.com/v1/recommendations', headers = headers, params = params)
    return parse_response(songs.text)

def parse_response(recommendations):
    r = json.loads(recommendations)
    song_list = r['tracks']
    song_objects = []
    for song in song_list:
        item = {
                'spotify_id': song['id'],
                'title': song['name'],
                'artist': song['artists'][0]['name'],
                'album': song['album']['name'],
                'spotify_url': song['external_urls']['spotify'],
                'album_art_url': song['album']['images'][0]['url'],
                'length': song['duration_ms']
               }

        song_objects.append(item)

    return jsonify(song_objects)

if __name__ == '__main__':
    api.run(debug=True)
