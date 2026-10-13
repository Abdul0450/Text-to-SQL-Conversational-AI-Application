import pyaudio
import websocket
import json
import threading
from urllib.parse import urlencode

## Confrigation
ASSEMBLYAI_KEY=""
API_ENDPOINT=F"wss://streaming.assemblyai.com/v3/ws?{urlencode({'sample_rate':16000})}"

CHUNK=800
RATE=16000
FORMAT=pyaudio.paInt16
CHAANEL=1

##GLOBAL
latest_text=""
text_lock=threading.Lock()
is_runing=False

##CALL_BACK
def meassage_on(ws,message):
    global latest_text
    try:
        data=json.loads(message)
        if data.get('type') == True and data.get("trun_is_formatted"):
            text=data["transcript"]
            with text_lock:
                latest_test=text

            print(f"[LIVE]{text}")
    except:
        pass

def on_open(ws):
    def stream_audio():
        p = pyaudio.PyAudio()
        stream=p.open(format=FORMAT,channels=CHAANEL,rate=RATE,input=True,frames_per_buffer=CHUNK)
        while is_runing:
            try:
                data=stream.read(CHUNK,exception_on_overflow=False)
                ws.send(data,websocket.ABNF.OPCODE_BINARY)
            except:
                break
            stream.stop_stream()
            stream.close()
            p.terminate()
    threading.Thread(target=stream_audio, daemon=True).start()

def on_error(ws,err):
    print(f"Error:{err}")

def on_close(*args):
    global is_runing
    is_runing=False
    print('Transcription stopped.')

##__PUBLIC__FUNCTIONS__
def start_transcription():
    



    

