import subprocess
from sanic import Sanic, response
# import os

app = Sanic(__name__)
app.ctx.restarting = False


@app.route("/")
async def test(_):
    return response.html(open("index.html", encoding='utf-8').read())


def is_github_request(request):
    # check if the request is from github, with the api key, the curl command is at the bottom of the file
    return request.headers.get("Authorization") == "Bearer " + "ABC123"



@app.route("/restart", methods=["POST"])
def webhook(request):
    # github actions posts to this endpoint, its @ the bottom of the file
    # check if the request is from github, with the api key, the curl command is at the bottom of the file
    if not is_github_request(request):
        return response.text("Not Authorized", status=401)

    subprocess.call(["git", "pull"])
    return response.text("Restarting")

    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=True)


# whats command to create requirements.txt
