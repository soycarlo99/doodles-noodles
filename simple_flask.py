import base64
import io
import threading
import time
import uuid
from datetime import datetime

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from PIL import Image, ImageOps

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")

# load ML stuff
model, scaler, labels = (
    joblib.load("quickdraw_model_50.joblib"),
    joblib.load("quickdraw_scaler_50.joblib"),
    joblib.load("quickdraw_classes_50.joblib"),
)

creatures = []  # list of dicts, oldest first
MAX = 20


# helpers
def to_creature(img_b64, artist):
    """Return (creature-dict, confidence) or (None, conf) if <0.5"""
    img = Image.open(io.BytesIO(base64.b64decode(img_b64.split(",")[1]))).convert(
        "L"
    )  # luminosity
    img = ImageOps.invert(img).resize((28, 28))
    X = scaler.transform(np.array(img, dtype=np.float32).reshape(1, -1) / 255.0)
    probs = model.predict_proba(X)[0]
    idx = int(np.argmax(probs))  # define first
    conf = float(probs[idx])  # use after
    if conf < 0.5:
        return None, conf
    cid = str(uuid.uuid4())
    typ = str(labels[idx])
    x = int(np.random.randint(50, 750))
    y = int(
        np.random.randint(250, 350) if typ == "fish" else np.random.randint(80, 200)
    )
    creature = dict(
        id=cid,
        img=img_b64,
        type=typ,
        conf=conf,
        artist=artist or "Anonymous",
        x=x,
        y=y,
        phase=float(np.random.random() * 6.28),
        dir=int(np.random.choice([-1, 1])) if typ == "fish" else 0,
        speed=float(np.random.uniform(1, 3)) if typ == "fish" else 0,
    )
    creature["born"] = datetime.now()
    # print(creature["born"]) example 2025-09-18 10:15:22.300955
    return creature, conf


# routes
@app.route("/")
def index():
    return render_template("indexsimple.html")


@app.route("/submit_creature", methods=["POST"])
def submit():
    creature, confidence = to_creature(
        request.json["image"], request.json.get("artist")
    )
    if creature is None:
        return jsonify(
            success=False,
            message=f"Only {confidence*100:.0f}% sure. Draw more clearly!",
        )
    if len(creatures) >= MAX:  # remove oldest
        creatures.sort(key=lambda c: c["born"])
        oldest = creatures.pop(0)
        sio.emit("remove", {"id": oldest["id"]})
    creatures.append(creature)
    sio.emit("add", {k: v for k, v in creature.items() if k != "born"})  # no datetime
    msg = f'{confidence*100:.0f}% {creature["type"]}! ' + (
        "It swims!" if creature["type"] == "fish" else "It parties!"
    )
    return jsonify(success=True, message=msg)


# socket
@sio.on("connect")
def send_all():
    for c in creatures:
        emit("add", {k: v for k, v in c.items() if k != "born"})


# game loop
def game_loop():
    while True:
        time.sleep(0.05)
        for c in creatures:
            if c["type"] == "fish":
                c["x"] += c["dir"] * c["speed"]
                if c["x"] <= 30:
                    c["x"], c["dir"] = 30, 1
                if c["x"] >= 770:
                    c["x"], c["dir"] = 770, -1
            c["phase"] = (c["phase"] + 0.1) % 6.28
        if creatures:
            sio.emit(
                "upd",
                {
                    c["id"]: dict(x=c["x"], y=c["y"], phase=c["phase"], dir=c["dir"])
                    for c in creatures
                },
            )


threading.Thread(target=game_loop, daemon=True).start()

# run
sio.run(app, debug=True, port=5002)
