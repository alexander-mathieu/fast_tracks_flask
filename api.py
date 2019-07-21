import os
from flask import Flask, request, jsonify, json
import requests
import config
import base64
import settings

api = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

@api.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the FastTracks Microservice!</h1>"

@api.route('/api/v1/recommended', methods=['GET'])
def parse_request():
    ids = request.args.get('song_ids')
    limit = request.args.get('limit')
    return get_recommended_songs(ids, limit)

def get_token():
    params = { 'grant_type': 'client_credentials' }
    r = requests.post('https://accounts.spotify.com/api/token', auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), data = params)
    json = r.json()
    token = json['access_token']
    return token

def get_recommended_songs(ids, limit):
    spotify_headers = get_token()
    params = { 'seed_tracks': ids.strip(), 'limit': limit }
    headers = { 'Authorization': f'Bearer {spotify_headers}' }
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
    api.run()
