#!/usr/bin/env python3

import os
import base64
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import torch
import numpy as np
import tensorflow as tf
from scipy.io import wavfile
import io
from nemo.collections.tts.models import TalkNetSpectModel
from nemo.collections.tts.models import TalkNetPitchModel
from nemo.collections.tts.models import TalkNetDursModel
from core.talknet_singer import TalkNetSingerModel
import json
import traceback
import ffmpeg
import time
import uuid
from core import extract, vocoder, reconstruct
from core.download import download_from_drive
from flask import request, send_file, make_response, abort

app = JupyterDash(__name__)

def getSilentWav():
  f = open("assets/silent.wav", "rb")
  buffer = io.BytesIO(f.read())
  return buffer

def mkResponse(data):
  return make_response(send_file(
    data,
    attachment_filename="audio.wav",
    mimetype="audio/x-wav",
  ))

@app.server.route("/tts")
def home():
    s = request.args.get("s")
    response = None
    if s is None or s == "":
        response = mkResponse(getSilentWav())
    else:
        voice = request.args.get('voice')
        if voice is None or voice == "":
            voice = "1k3EMXxLC0fLvfxzGbeP6B6plgu9hqCSx"
        response = mkResponse(generate_audio2(1, voice + "|default", None, s, [], 0, None, None, None))
    # res.setHeader('Access-Control-Allow-Origin', '*');
    # res.setHeader('Access-Control-Allow-Headers', '*');
    # res.setHeader('Access-Control-Allow-Methods', '*');
    # res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
    # res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
    # res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

DEVICE = "cuda:0"
CPU_PITCH = False
RUN_PATH = os.path.dirname(os.path.realpath(__file__))
if RUN_PATH == "/content":
    UI_MODE = "colab"
elif os.path.exists("/talknet/is_docker"):
    UI_MODE = "docker"
else:
    UI_MODE = "offline"
torch.set_grad_enabled(False)
if CPU_PITCH:
    tf.config.set_visible_devices([], "GPU")

extract_dur = extract.ExtractDuration(RUN_PATH, DEVICE)
extract_pitch = extract.ExtractPitch()
reconstruct_inst = reconstruct.Reconstruct(
    DEVICE,
    os.path.join(
        RUN_PATH,
        "core",
        "vqgan_config.yaml",
    ),
    os.path.join(
        RUN_PATH,
        "models",
        "vqgan32_universal_57000.ckpt",
    ),
)

app.title = "Webaverse TTS"
app.layout = html.Div(
    children=[
        html.H1(
            id="header",
            children="Webaverse TTS",
            style={
                "color": "#52042c",
                "font-size": "4em",
                "text-align": "center",
                "margin-top": "0em",
                "margin-bottom": "0em",
            },
        ),
        html.Label("Character selection", htmlFor="model-dropdown"),
        dbc.Select(
            id="model-dropdown",
            options=[
                {
                    "label": "Custom model",
                    "value": "Custom",
                },
                {
                    "label": "--- ERROR LOADING MODEL LISTS ---",
                    "value": "",
                    "disabled": True,
                },
            ],
            value=None,
            style={
                "max-width": "90vw",
                "width": "35em",
                "margin-bottom": "0.7em",
            },
        ),
        html.Div(
            children=[
                dcc.Input(
                    id="drive-id",
                    type="text",
                    placeholder="Drive ID for custom model",
                    style={"width": "22em"},
                ),
            ],
            id="custom-model",
            style={
                "display": "none",
            },
        ),
        dcc.Store(id="current-f0s"),
        dcc.Store(id="current-f0s-nosilence"),
        dcc.Store(id="current-filename"),
        dcc.Loading(
            id="audio-loading",
            children=[
                html.Div(
                    [
                        html.Button(
                            "Update file list",
                            id="update-button",
                            style={
                                "margin-right": "10px",
                            },
                        ),
                        dbc.Select(
                            id="reference-dropdown",
                            options=[],
                            value=None,
                            style={
                                "max-width": "80vw",
                                "width": "30em",
                            },
                            disabled=False,
                        )
                    ],
                    style={
                        "width": "100%",
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "flex-direction": "row",
                        "margin-left": "50px",
                        "vertical-align": "middle",
                    },
                ),
                html.Audio(
                    id="pitch-out",
                    controls=True,
                    style={"display": "none"},
                ),
                html.Div(
                    id="audio-loading-output",
                    style={
                        "font-style": "italic",
                        "margin-bottom": "0.7em",
                        "text-align": "center",
                    },
                ),
            ],
            type="default",
        ),
        html.Label("Transcript", htmlFor="transcript-input"),
        dcc.Textarea(
            id="transcript-input",
            value="",
            style={
                "max-width": "90vw",
                "width": "50em",
                "height": "8em",
                "margin-bottom": "0.7em",
            },
        ),
        dcc.Loading(
            html.Div(
                [
                    html.Button(
                        "Generate",
                        id="gen-button",
                    ),
                    html.Audio(
                        id="audio-out",
                        controls=True,
                        style={
                            "display": "none",
                        },
                    ),
                    html.Div(
                        id="generated-info",
                        style={
                            "font-style": "italic",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "flex-direction": "column",
                },
            )
        )
    ],
    style={
        "width": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
        "flex-direction": "column",
        "background-color": "#FFF",
    },
)

upload_display = {
    "width": "100%",
    "height": "60px",
    "lineHeight": "60px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "5px",
    "textAlign": "center",
    "margin": "10px",
}

playback_style = {
    "margin-top": "0.3em",
    "margin-bottom": "0.3em",
    "display": "block",
    "width": "600px",
    "max-width": "90vw",
}

playback_hide = {
    "display": "none",
}


@app.callback(
    dash.dependencies.Output("modal", "is_open"),
    [
        dash.dependencies.Input("open", "n_clicks"),
        dash.dependencies.Input("close", "n_clicks"),
    ],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [
        dash.dependencies.Output("model-dropdown", "options"),
        dash.dependencies.Output("upload-audio", "style"),
    ],
    dash.dependencies.Input("header", "children"),
)
def init_dropdown(value):
    if UI_MODE == "docker":
        upload_style = upload_display
    else:
        upload_style = playback_hide

    dropdown = [
        {
            "label": "Custom model",
            "value": "Custom|default",
        }
    ]
    prev_values = ["Custom|default"]

    def add_to_dropdown(entry):
        if entry["value"] in prev_values:
            return
        dropdown.append(entry)
        prev_values.append(entry["value"])

    all_dict = {}
    for filename in os.listdir("model_lists"):
        if len(filename) < 5 or filename[-5:].lower() != ".json":
            continue
        with open(os.path.join("model_lists", filename)) as f:
            j = json.load(f)
            for s in j:
                for c in s["characters"]:
                    c["source_file"] = filename[:-5]
                if s["source"] not in all_dict:
                    all_dict[s["source"]] = s["characters"]
                else:
                    all_dict[s["source"]].extend(s["characters"])
    for k in sorted(all_dict):
        seen_chars = []
        seen_ids = []
        characters = {}
        characters_sing = {}
        has_singers = False
        for c in all_dict[k]:
            if c["drive_id"] in seen_ids:
                continue
            seen_ids.append(c["drive_id"])
            # Handle duplicate names
            if c["name"] in seen_chars:
                if c["name"] in characters:
                    rename = (
                        c["name"] + " [" + characters[c["name"]]["source_file"] + "]"
                    )
                    characters[rename] = characters[c["name"]]
                    del characters[c["name"]]
                c["name"] = c["name"] + " [" + c["source_file"] + "]"
            else:
                seen_chars.append(c["name"])

            characters[c["name"]] = {
                "drive_id": c["drive_id"],
                "is_singing": c["is_singing"],
                "source_file": c["source_file"],
            }
            if c["is_singing"]:
                has_singers = True
        if has_singers:
            for ck in sorted(characters):
                if characters[ck]["is_singing"]:
                    characters_sing[ck] = characters[ck]
                    del characters[ck]
            separator = "--- " + k.strip().upper() + " MODELS (TALKING) ---"
        else:
            separator = "--- " + k.strip().upper() + " MODELS ---"
        if len(characters) > 0:
            add_to_dropdown(
                {
                    "label": separator,
                    "value": str(uuid.uuid4()) + "|default",
                    "disabled": True,
                }
            )
            for ck in sorted(characters):
                add_to_dropdown(
                    {
                        "label": ck,
                        "value": characters[ck]["drive_id"] + "|default",
                    }
                )
        if has_singers:
            separator = "--- " + k.strip().upper() + " MODELS (SINGING) ---"
            add_to_dropdown(
                {
                    "label": separator,
                    "value": str(uuid.uuid4()) + "|default",
                    "disabled": True,
                }
            )
            for ck in sorted(characters_sing):
                add_to_dropdown(
                    {
                        "label": ck,
                        "value": characters_sing[ck]["drive_id"] + "|singing",
                    }
                )
    if len(all_dict) == 0:
        add_to_dropdown(
            {
                "label": "--- NO MODEL LISTS FOUND ---",
                "value": str(uuid.uuid4()) + "|default",
                "disabled": True,
            }
        )
    return [dropdown, upload_style]


@app.callback(
    dash.dependencies.Output("custom-model", "style"),
    dash.dependencies.Input("model-dropdown", "value"),
)
def update_model(model):
    if model is not None and model.split("|")[0] == "Custom":
        style = {"margin-bottom": "0.7em", "display": "block"}
    else:
        style = {"display": "none"}
    return style


@app.callback(
    [
        dash.dependencies.Output("pitch-factor", "disabled"),
        dash.dependencies.Output("reference-dropdown", "disabled"),
        dash.dependencies.Output("pitch-button", "disabled"),
    ],
    [
        dash.dependencies.Input("pitch-options", "value"),
    ],
)


@app.callback(
    dash.dependencies.Output("upload-label", "children"),
    [
        dash.dependencies.Input("upload-audio", "filename"),
        dash.dependencies.Input("upload-audio", "contents"),
    ],
)
def save_upload(uploaded_filenames, uploaded_file_contents):
    try:
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, content in zip(uploaded_filenames, uploaded_file_contents):
                if name.strip() == "":
                    continue
                data = content.encode("utf8").split(b";base64,")[1]
                with open(os.path.join(RUN_PATH, name), "wb") as fp:
                    fp.write(base64.decodebytes(data))
    except Exception as e:
        return str(e)
    return "Uploaded " + str(len(uploaded_filenames)) + " file(s)"


@app.callback(
    dash.dependencies.Output("reference-dropdown", "options"),
    [
        dash.dependencies.Input("update-button", "n_clicks"),
    ],
)
def update_filelist(n_clicks):
    filelist = []
    supported_formats = [".wav", ".ogg", ".mp3", "flac", ".aac"]
    for x in sorted(os.listdir(RUN_PATH)):
        if x[-4:].lower() in supported_formats:
            filelist.append({"label": x, "value": x})
    return filelist


@app.callback(
    [
        dash.dependencies.Output("audio-loading-output", "children"),
        dash.dependencies.Output("current-f0s", "data"),
        dash.dependencies.Output("current-f0s-nosilence", "data"),
        dash.dependencies.Output("current-filename", "data"),
    ],
    [
        dash.dependencies.Input("reference-dropdown", "value"),
    ],
    [dash.dependencies.State("pitch-options", "value")],
)
def select_file(dropdown_value, pitch_options):
    if dropdown_value is not None:
        if not os.path.exists(os.path.join(RUN_PATH, "temp")):
            os.mkdir(os.path.join(RUN_PATH, "temp"))
        ffmpeg.input(os.path.join(RUN_PATH, dropdown_value)).output(
            os.path.join(RUN_PATH, "temp", dropdown_value + "_conv.wav"),
            ar="22050",
            ac="1",
            acodec="pcm_s16le",
            map_metadata="-1",
            fflags="+bitexact",
        ).overwrite_output().run(quiet=True)
        if "pitch" in pitch_options:
            f0_with_silence, f0_wo_silence = extract_pitch.get_pitch(
                os.path.join(RUN_PATH, "temp", dropdown_value + "_conv.wav"),
                legacy=False,
            )
        else:
            f0_with_silence, f0_wo_silence = extract_pitch.get_pitch(
                os.path.join(RUN_PATH, "temp", dropdown_value + "_conv.wav"),
                legacy=True,
            )
        return [
            "Analyzed " + dropdown_value,
            f0_with_silence,
            f0_wo_silence,
            dropdown_value,
        ]
    else:
        return ["No audio analyzed", None, None]


@app.callback(
    [
        dash.dependencies.Output("pitch-out", "src"),
        dash.dependencies.Output("pitch-out", "style"),
        dash.dependencies.Output("pitch-clicks", "data"),
    ],
    [
        dash.dependencies.Input("pitch-button", "n_clicks"),
        dash.dependencies.Input("pitch-clicks", "data"),
        dash.dependencies.Input("current-f0s", "data"),
    ],
)
def debug_pitch(n_clicks, pitch_clicks, current_f0s):
    if not n_clicks or current_f0s is None or n_clicks <= pitch_clicks:
        if n_clicks is not None:
            pitch_clicks = n_clicks
        else:
            pitch_clicks = 0
        return [
            None,
            playback_hide,
            pitch_clicks,
        ]
    pitch_clicks = n_clicks
    return [extract_pitch.f0_to_audio(current_f0s), playback_style, pitch_clicks]


tnmodels, tnmodel, tnpath, tndurs, tnpitch = {}, None, None, None, None
voc, last_voc, sr_voc, rec_voc = None, None, None, None


@app.callback(
    [
        dash.dependencies.Output("audio-out", "src"),
        dash.dependencies.Output("generated-info", "children"),
        dash.dependencies.Output("audio-out", "style"),
        dash.dependencies.Output("audio-out", "title"),
    ],
    [dash.dependencies.Input("gen-button", "n_clicks")],
    [
        dash.dependencies.State("model-dropdown", "value"),
        dash.dependencies.State("drive-id", "value"),
        dash.dependencies.State("transcript-input", "value"),
        dash.dependencies.State("pitch-options", "value"),
        dash.dependencies.State("pitch-factor", "value"),
        dash.dependencies.State("current-filename", "data"),
        dash.dependencies.State("current-f0s", "data"),
        dash.dependencies.State("current-f0s-nosilence", "data"),
    ],
)
def generate_audio(
    n_clicks,
    model,
    custom_model,
    transcript,
    pitch_options,
    pitch_factor,
    wav_name,
    f0s,
    f0s_wo_silence,
):
    global tnmodels, tnmodel, tnpath, tndurs, tnpitch, voc, last_voc, sr_voc, rec_voc
    # n_clicks, model, custom_model, transcript, pitch_options, pitch_factor, wav_name, f0s, f0s_wo_silence,
    # 1 1UFQWJHzKFPumoxioopPbAzM9ydznnRX3|default None "fsdg" ['dra'] 0 None None None
    # 1 132G6oD0HHPPn4t1H6IkYv18_F0UVLWgi|default None "got it and lol" ['dra'] 0 None None None
    # with open('readme.txt', 'w') as f:
    #   f.write("%s %s %s %s %s %s %s %s %s" % (n_clicks, model, custom_model, transcript, pitch_options, pitch_factor, wav_name, f0s, f0s_wo_silence))

    if n_clicks is None:
        raise PreventUpdate
    if model is None:
        return [None, "No character selected", playback_hide, None]
    if transcript is None or transcript.strip() == "":
        return [
            None,
            "No transcript entered",
            playback_hide,
            None,
        ]
    load_error, talknet_path, vocoder_path = download_from_drive(
        model.split("|")[0], custom_model, RUN_PATH
    )
    if load_error is not None:
        return [
            None,
            load_error,
            playback_hide,
            None,
        ]

    try:
        with torch.no_grad():
            tnmodel = tnmodels.get(talknet_path)
            if tnmodel is None:
                # if tnpath != talknet_path:
                    singer_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetSinger.nemo"
                    )
                    if os.path.exists(singer_path):
                        tnmodel = TalkNetSingerModel.restore_from(singer_path)
                    else:
                        tnmodel = TalkNetSpectModel.restore_from(talknet_path)
                    durs_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetDurs.nemo"
                    )
                    pitch_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetPitch.nemo"
                    )
                    if os.path.exists(durs_path):
                        tndurs = TalkNetDursModel.restore_from(durs_path)
                        tnmodel.add_module("_durs_model", tndurs)
                        tnpitch = TalkNetPitchModel.restore_from(pitch_path)
                        tnmodel.add_module("_pitch_model", tnpitch)
                    else:
                        tndurs = None
                        tnpitch = None
                    tnmodel.eval()
                    tnpath = talknet_path
                    tnmodels[talknet_path] = tnmodel

            # Generate spectrogram
            token_list, tokens, arpa = extract_dur.get_tokens(transcript)
            if tndurs is None or tnpitch is None:
                return [
                    None,
                    "Model doesn't support pitch prediction",
                    playback_hide,
                    None,
                ]
            # Vocoding
            if last_voc != vocoder_path:
                voc = vocoder.HiFiGAN(vocoder_path, "config_v1", DEVICE)
                last_voc = vocoder_path
            audio, audio_torch = voc.vocode(spect)

            # Reconstruction
            if "srec" in pitch_options:
                new_spect = reconstruct_inst.reconstruct(spect)
                if rec_voc is None:
                    rec_voc = vocoder.HiFiGAN(
                        os.path.join(RUN_PATH, "models", "hifirec"), "config_v1", DEVICE
                    )
                audio, audio_torch = rec_voc.vocode(new_spect)

            # Super-resolution
            if sr_voc is None:
                sr_voc = vocoder.HiFiGAN(
                    os.path.join(RUN_PATH, "models", "hifisr"), "config_32k", DEVICE
                )
            sr_mix, new_rate = sr_voc.superres(audio, 22050)

            # Create buffer
            buffer = io.BytesIO()
            wavfile.write(buffer, new_rate, sr_mix.astype(np.int16))
            b64 = base64.b64encode(buffer.getvalue())
            sound = "data:audio/x-wav;base64," + b64.decode("ascii")

            output_name = "TalkNet_" + str(int(time.time()))
            return [sound, arpa, playback_style, output_name]
    except Exception:
        return [
            None,
            str(traceback.format_exc()),
            playback_hide,
            None,
        ]

def generate_audio2(
    n_clicks,
    model,
    custom_model,
    transcript,
    pitch_options,
    pitch_factor,
    wav_name,
    f0s,
    f0s_wo_silence,
):
    global tnmodels, tnpath, tndurs, tnpitch, voc, last_voc, sr_voc, rec_voc
    # n_clicks, model, custom_model, transcript, pitch_options, pitch_factor, wav_name, f0s, f0s_wo_silence,
    # 1 1UFQWJHzKFPumoxioopPbAzM9ydznnRX3|default None "fsdg" ['dra'] 0 None None None
    # 1 132G6oD0HHPPn4t1H6IkYv18_F0UVLWgi|default None "got it and lol" ['dra'] 0 None None None
    # with open('readme.txt', 'w') as f:
    #   f.write("%s %s %s %s %s %s %s %s %s" % (n_clicks, model, custom_model, transcript, pitch_options, pitch_factor, wav_name, f0s, f0s_wo_silence))

    if n_clicks is None:
        raise PreventUpdate
    if model is None:
        return [None, "No character selected", playback_hide, None]
    if transcript is None or transcript.strip() == "":
        return [
            None,
            "No transcript entered",
            playback_hide,
            None,
        ]
    load_error, talknet_path, vocoder_path = download_from_drive(
        model.split("|")[0], custom_model, RUN_PATH
    )
    if load_error is not None:
        return [
            None,
            load_error,
            playback_hide,
            None,
        ]

    try:
        with torch.no_grad():
            tnmodel = tnmodels.get(talknet_path)
            if tnmodel is None:
                # if tnpath != talknet_path:
                    singer_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetSinger.nemo"
                    )
                    if os.path.exists(singer_path):
                        tnmodel = TalkNetSingerModel.restore_from(singer_path)
                    else:
                        tnmodel = TalkNetSpectModel.restore_from(talknet_path)
                    durs_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetDurs.nemo"
                    )
                    pitch_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetPitch.nemo"
                    )
                    if os.path.exists(durs_path):
                        tndurs = TalkNetDursModel.restore_from(durs_path)
                        tnmodel.add_module("_durs_model", tndurs)
                        tnpitch = TalkNetPitchModel.restore_from(pitch_path)
                        tnmodel.add_module("_pitch_model", tnpitch)
                    else:
                        tndurs = None
                        tnpitch = None
                    tnmodel.eval()
                    tnpath = talknet_path
                    tnmodels[talknet_path] = tnmodel

            # Generate spectrogram
            try:
                token_list, tokens, arpa = extract_dur.get_tokens(transcript)
                if tndurs is None or tnpitch is None:
                    return [
                        None,
                        "Model doesn't support pitch prediction",
                        playback_hide,
                        None,
                    ]
                spect = tnmodel.generate_spectrogram(tokens=tokens)
                # Vocoding
                if last_voc != vocoder_path:
                    voc = vocoder.HiFiGAN(vocoder_path, "config_v1", DEVICE)
                    last_voc = vocoder_path
                audio, audio_torch = voc.vocode(spect)

                # Reconstruction
                if "srec" in pitch_options:
                    new_spect = reconstruct_inst.reconstruct(spect)
                    if rec_voc is None:
                        rec_voc = vocoder.HiFiGAN(
                            os.path.join(RUN_PATH, "models", "hifirec"), "config_v1", DEVICE
                        )
                    audio, audio_torch = rec_voc.vocode(new_spect)

                # Super-resolution
                if sr_voc is None:
                    sr_voc = vocoder.HiFiGAN(
                        os.path.join(RUN_PATH, "models", "hifisr"), "config_32k", DEVICE
                    )
                sr_mix, new_rate = sr_voc.superres(audio, 22050)

                # Create buffer
                buffer = io.BytesIO()
                wavfile.write(buffer, new_rate, sr_mix.astype(np.int16))
                return buffer
                # b64 = base64.b64encode(buffer.getvalue())
                # sound = "data:audio/x-wav;base64," + b64.decode("ascii")

                # output_name = "TalkNet_" + str(int(time.time()))
                # return [sound, arpa, playback_style, output_name]
            except IndexError:
                return getSilentWav()
    except Exception:
        return str(traceback.format_exc())

if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=8080,
        mode="external",
        debug=False,
        # dev_tools_silence_routes_logging = False,
        # dev_tools_ui=True,
        # dev_tools_hot_reload=True,
        threaded=True,
    )
