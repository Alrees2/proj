import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def youtube_search(query):
    url = "https://youtube-v38.p.rapidapi.com/search/"
    headers = {
        'x-rapidapi-host': "youtube-v38.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }
    params = {
        'q': query,
        'hl': 'en',
        'gl': 'US'
    }
    response = requests.get(url, headers=headers, params=params)
    results = response.json()

    output = []
    for item in results.get('items', []):
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        
        # Check if title or channel starts with the query entirely (case insensitive)
        if title.lower().startswith(query.lower()) or channel.lower().startswith(query.lower()):
            video_info = {
                "title": title,
                "channel": channel,
            }
            if 'videoId' in item['id']:
                video_info["url"] = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            elif 'channelId' in item['id']:
                video_info["url"] = f"https://www.youtube.com/channel/{item['id']['channelId']}"
            output.append(video_info)
    
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        results = youtube_search(query)
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بحث يوتيوب</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { width: 50%; margin: auto; }
            h1 { text-align: center; }
            form { text-align: center; margin-bottom: 20px; }
            input[type="text"] { padding: 10px; width: 80%; }
            input[type="submit"] { padding: 10px 20px; }
            .results { margin-top: 20px; }
            .video { margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }
            .video a { text-decoration: none; color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>بحث يوتيوب</h1>
            <form method="post">
                <input type="text" name="query" placeholder="أدخل حرف للبحث" value="{{ query }}" required>
                <input type="submit" value="بحث">
            </form>
            <div class="results">
                {% if results %}
                    {% for result in results %}
                        <div class="video">
                            <h2><a href="{{ result.url }}" target="_blank">{{ result.title }}</a></h2>
                            <p>القناة: {{ result.channel }}</p>
                        </div>
                    {% endfor %}
                {% else %}
                    <p>لا توجد نتائج للبحث</p>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    ''', query=query, results=results)

if __name__ == '__main__':
    os.environ['RAPIDAPI_KEY'] = '31e9ec85c2msh9116a6083229fe1p11e8c1jsnf0bedf7ed664'
    app.run(debug=True)
