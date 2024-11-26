from fastapi import FastAPI
import json
import umgxspot as spothelper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://0.0.0.0:8080", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"hello": "umang"}


@app.get("/playlist/{id}")
def read_playlist(id: str):
    dump_link = "https://open.spotify.com/playlist/" + id
    helper = spothelper.playlist(dump_link)
    if helper.validate_link() == False:
        return {"Error": "Check the tag"}
    else:
        playlist_json = helper.get_playlist_json()
        return json.loads(playlist_json)


@app.get("/link/{id}")
def gen_link(id):
    dump_link = "spotdl url https://open.spotify.com/track/" + id
    import subprocess
    command_output = subprocess.getoutput(dump_link)
    command_output = command_output.split("\n", 1)[1]
    return {"link": command_output}

@app.get("/covers/{id}")
def gen_covers(id):
    dump_link = "https://open.spotify.com/playlist/" + id
    helper = spothelper.playlist(dump_link)
    if helper.validate_link() == False:
       return {"Error":"Check The Tag"}
    #work in progress and make it json as the returned object is python list
