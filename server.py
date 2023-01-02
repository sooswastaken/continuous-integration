from sanic import Sanic, response
import os
import sys
import time
import asyncio
import subprocess
from hmac import HMAC, compare_digest
from hashlib import sha1


app = Sanic(__name__)
app.ctx.restarting = False


@app.route("/")
async def test(_):
    return response.text(open("server.py").read())


def verify_signature(req):
    received_sign = req.headers.get("X-Hub-Signature").split("sha1=")[-1].strip()
    secret = "ABCD123".encode()
    expected_sign = HMAC(key=secret, msg=req.body, digestmod=sha1).hexdigest()
    return compare_digest(received_sign, expected_sign)


@app.route("/listen", methods=["POST"])
def webhook(request):
    if verify_signature(request):
        # check if repo is correct
        if (
            request.json.get("repository").get("full_name")
            == "sooswastaken/continuous-integration"
        ):
            # git pull
            app.ctx.restarting = True
            os.system("git pull")
            # error or success
            if app.ctx.restarting:
                return response.text("Internal Server Error", status=500)
            else:
                return response.text("OK", status=200)
    return response.text("Forbidden", status=403)


@app.listener("before_server_start")
async def start_server(app, loop):
    app.ctx.restarting = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=True)
