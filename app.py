from flask import Flask, request, render_template
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = youtube_search(query)
    return render_template('results.html', results=results)

def youtube_search(query):
    url = "https://youtube.googleapis.com/youtube/v3/search"
    api_key = os.getenv('31e9ec85c2msh9116a6083229fe1p11e8c1jsnf0bedf7ed664')  # Fetch API key from environment variable

    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video,channel',
        'key': api_key,
        'maxResults': 10
    }

    response = requests.get(url, params=params)
    results = response.json()

    output = []
    for item in results.get('items', []):
        title = item['snippet']['title']
        if 'videoId' in item['id']:
            output.append({"type": "Video", "title": title, "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"})
        elif 'channelId' in item['id']:
            output.append({"type": "Channel", "title": title, "url": f"https://www.youtube.com/channel/{item['id']['channelId']}"})

    return output

if __name__ == '__main__':
    app.run(debug=True)
