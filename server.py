from sanic import Sanic, response
import os

app = Sanic(__name__)
app.ctx.restarting = False


@app.route("/")
async def test(_):
    return response.html(open("server.py").read())


def is_github_request(request):
    # check if the request is from github, with the api key, the curl command is at the bottom of the file
    return request.headers.get("Authorization") == "Bearer " + "ABC123"



@app.route("/restart", methods=["POST"])
def webhook(request):
    # github actions posts to this endpoint, its @ the bottom of the file
    # check if the request is from github, with the api key, the curl command is at the bottom of the file
    if not is_github_request(request):
        return response.text("Not Authorized", status=401)
    
    # run git pull, which automatically restarts the server
    os.system("git pull")

    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=True)
# name: Lint and call API

# on: [push]

# jobs:
#   lint:
#     runs-on: ubuntu-latest
#     steps:
#       # ... steps to lint code with flake8

#   call-api:
#     runs-on: ubuntu-latest
#     needs: [lint]
#     steps:
#       - name: Set API key
#         run: echo "::set-env name=API_KEY::${{ secrets.API_KEY }}"
#       - name: Call API
#         run: |
#           # Call your API here, using the API key stored in the API_KEY environment variable
#           curl -X POST https://api.example.com/endpoint -H "Authorization: Bearer $API_KEY"