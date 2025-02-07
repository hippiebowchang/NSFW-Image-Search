from flask import Flask, request, render_template, redirect
import requests
import os

app = Flask(__name__)
import logging
logging.basicConfig(level=logging.DEBUG)


# Imgbb API Key (Make sure to replace this with yours if needed)
IMGBB_API_KEY = "d516255c6bd11f68fb3f02d1983c4351"

# Search Engine URLs
SEARCH_ENGINES = {
    "google": "https://www.google.com/searchbyimage?image_url=",
    "bing": "https://www.bing.com/images/search?q=imgurl:",
    "yandex": "https://yandex.com/images/search?rpt=imageview&url=",
    "saucenao": "https://saucenao.com/search.php?db=999&url=",
    "tineye": "https://tineye.com/search?url=",
    "dropexo": "https://dropexo.com/search?query=",
    "mmsdose": "https://www.mmsdose.com/search?query=",
    "nsfwsearch": "https://nsfw-search.com/search?query="  # Example NSFW search engine
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    # Upload image to Imgbb
    response = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY},
        files={"image": file}
    )
    
    if response.status_code != 200:
        return "Image upload failed", 500
    
    image_url = response.json()['data']['url']
    search_engine = request.form.get("engine")
    
    if search_engine not in SEARCH_ENGINES:
        return "Invalid search engine selected", 400
    
    # Redirect to search engine with uploaded image URL
    search_url = SEARCH_ENGINES[search_engine] + image_url
    return redirect(search_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
