from sanic import Sanic, response
import os
import sys
import time
import asyncio
import subprocess
from hmac import HMAC, compare_digest
from hashlib import sha1


app = Sanic(__name__)


@app.route("/")
async def test(_):
    return response.html(open("index.html").read())


async def quit():
    try:
        app.stop()
        subprocess.Popen(["sh", "./start.sh"])
        sys.exit(0)
    except Exception as e:
        print(e)


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
            asyncio.create_task(quit())
            return response.text("Restarting...", status=200)
    return response.text("Forbidden", status=403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
