import subprocess
from typing import List, Optional, Union
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from config import config
from schemas import SpeakerUpdate
from speakers import Speaker
from speakers.sonos import Sonos
from templates import templates


class JackcastCtl:
    """The intent of this class is to be the master controller for Jackcast.
    As we expand to support additional network speakers the"""

    def __init__(self) -> None:
        # The master volume
        self.volume: int = 0  # The currently active speaker implementing a AudioNetwork class
        self.speaker: Optional[Sonos] = None


jc = JackcastCtl()
jc.speaker = Sonos(80)


api = FastAPI(title="Phonocast", version="0.1.0")
api.mount("/static", StaticFiles(directory=config.STATIC_PATH), name="static")


@api.get("/cast")
async def cast():
    def stream_audio_from_sink():
        # The following will proxy the null sink to the network
        # This strategy was obtained from the following resources,
        # * https://askubuntu.com/questions/60837/record-a-programs-output-with-
        # pulseaudio
        # * mkchromecast

        # Pulseaudio names the monitor after the module name appended with
        # '.monitor'.
        monitor_name = f"{config.PULSE_AUDIO_SINK_NAME}.monitor"
        # Record raw audio coming from the monitoring sink and output to stdout
        parec = subprocess.Popen(["parec", "--format=s16le", "-d", monitor_name], stdout=subprocess.PIPE)
        # Encode the raw audio recording to mp3 and output to stdout
        lame = subprocess.Popen(["lame", "-b", "192", "-r", "-"], stdin=parec.stdout, stdout=subprocess.PIPE)
        buf_size = 8192
        while True:
            yield lame.stdout.read(buf_size)

    return StreamingResponse(stream_audio_from_sink(), media_type="audio/mp3")


@api.get("/api/volume")
async def get_volume():
    return {"success": True, "volume": jc.speaker.volume}


@api.post("/api/volume")
async def set_volume(request: Request):
    volume = await request.form.__dict__["volume"]
    print("Volume =", volume)
    jc.volume = volume
    jc.speaker.set_volume(volume)
    return {"success": True, "volume": jc.speaker.volume}


@api.post("/api/speakers")
async def set_speakers(request: Request):
    form_data = await request.form()
    devices = form_data.get("devices[]", [])
    if len(devices) > 0:
        devices = [devices]
        # no grouping just play on that speaker
        jc.speaker.set_active(devices)
        jc.speaker.set_volume(jc.volume)
        jc.speaker.play()
    else:
        jc.speaker.stop()
        jc.speaker.set_active([])

    return {"success": True, "device": {"volume": jc.speaker.volume}}


@api.get("/api/speakers")
def get_speakers():
    speakers = [vars(speaker) for speaker in jc.speaker.speakers()]

    return {"success": True, "speakers": speakers, "volume": jc.speaker.volume}


# @api.put("/api/speakers/{name}")
# def update_speaker(name: str, data: Optional[SpeakerUpdate]):
#
#


@api.route("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
