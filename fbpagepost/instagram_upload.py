import requests
import http.server
import socketserver
import threading
import subprocess
import time
import json

# Start a simple HTTP server in a new thread
PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()

# Start ngrok without specifying the full path
ngrok = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.PIPE)

# Give ngrok time to start up
time.sleep(2)

# Get the public URL from ngrok
resp = requests.get("http://localhost:4040/api/tunnels")
public_url = resp.json()["tunnels"][0]["public_url"]

# Now you can use the public URL to access your local images
image_url = public_url + "/test1.jpg"
print("Image URL:", image_url)

access_token = "EAAObL6GYdaABOxVDM58eAHihRiIymnSnxqDI5Fdj0ZBVZAKaZADGZCWd7LqOw7LhVceJky9dSzll9EjMCxLOJ2R902ZC9Q4ZAy4W2eYiBbwXH44c23ofvD9OY4711YjlmbbElF57ySa2J8nWZB8ZAoqIvZB771XATOT3Tj0mQcpTMvc20kAZAdy2EHj2EH9460M7xlaakoTcZArXVEV73OwlQZDZD"
instagram_id = "17841467174628931"
caption = "Best Movie from 2012"

def create_container(access_token, image_url, caption):
    url = f"https://graph.facebook.com/v17.0/{instagram_id}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    response = requests.post(url, params=payload)
    data = response.json()
    print("Create Container Response:", data)
    return data.get("id")

def publish_photo(access_token, creation_id):
    url = f"https://graph.facebook.com/v20.0/{instagram_id}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    response = requests.post(url, params=payload)
    data = response.json()
    print("Publish Photo Response:", data)

# Create and publish the photo
creation_id = create_container(access_token, image_url, caption)
if creation_id:
    publish_photo(access_token, creation_id)

# Remember to stop ngrok and the HTTP server when you're done
ngrok.terminate()
httpd.shutdown()
