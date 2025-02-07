from flask import Flask, request, redirect, render_template
import requests
import os

app = Flask(__name__)
import logging
logging.basicConfig(level=logging.DEBUG)


# Your ImgBB API Key
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "d516255c6bd11f68fb3f02d1983c4351")

# NSFW Search Engines
NSFW_SITES = {
    "Bing": "https://www.bing.com/images/search?q={query}",
    "Yandex": "https://yandex.com/images/search?rpt=imageview&url={image_url}",
    "Kivera": "https://kivera.site/search?url={image_url}",
    "Reddit": "https://www.reddit.com/search?q={query}&type=image",
    "DropMMS": "https://dropmms.com/search?url={image_url}",
    "MMSDose": "https://mmsdose.com/search?url={image_url}"
}

@app.route('/')
def home():
    return render_template('index.html', sites=NSFW_SITES.keys())

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    image = request.files['image']
    response = requests.post("https://api.imgbb.com/1/upload",
                             data={"key": IMGBB_API_KEY},
                             files={"image": image})
    
    if response.status_code != 200:
        return "Image upload failed", 500
    
    image_url = response.json()["data"]["url"]
    search_engine = request.form.get("search_engine")
    
    if search_engine not in NSFW_SITES:
        return "Invalid search engine selected", 400
    
    search_url = NSFW_SITES[search_engine].replace("{image_url}", image_url)
    
    return redirect(search_url)

if __name__ == '__main__':
    app.run(debug=True)
