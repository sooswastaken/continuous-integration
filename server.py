from sanic import Sanic, response
import os
import sys
import time
import asyncio

app = Sanic(__name__)

@app.route("/")
async def test(request):
    return response.html(open('index.html').read())

@app.route("/restart")
async def restart(request):
    asyncio.create_task(quit())
    return response.html("Restarting...")


async def quit():
    app.stop()
    os.system("sh start.sh")
    sys.exit(0)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)