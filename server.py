from sanic import Sanic, response
import os
import sys
import time
import asyncio
import subprocess


app = Sanic(__name__)

@app.route("/")
async def test(_):
    return response.html(open('index.html').read())

@app.route("/restart")
async def restart(_):
    asyncio.create_task(quit())
    return response.html("Restarting...")


async def quit():
    app.stop()
    subprocess.Popen(['sh', './start.sh'])
    sys.exit(0)

@app.post('/listen')
async def listen(request):
    """Listen for GitHub events"""
    print(request.json)
    return response.json({}, headers={'Content-Type': 'application/json'})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)