# 🖐️ Hand Tracker & Finger Counter

A real-time hand tracking script that opens your webcam, follows your hands, and counts how many fingers you're holding up — all using Python, OpenCV, and MediaPipe.

Supports **both hands at once**, works in a mirror-view so it feels natural, and draws a clean skeleton overlay on each hand.

---

## 📸 Demo

> Hold your hand up in front of the camera and the tracker will detect it, draw landmarks, and display the finger count in real time.

---

## ✨ Features

- 🎥 Live webcam feed with mirror view
- ✋ Tracks up to 2 hands simultaneously
- 🔢 Counts extended fingers per hand (0–5) and shows the total
- 💀 Draws the full hand skeleton (21 landmarks + connections)
- 🏷️ Labels each hand as **Left** or **Right** with its individual count
- ⚡ Runs fast using MediaPipe's lightweight model

---

## 🛠️ Requirements

- Python 3.8+
- A webcam

### Install dependencies

```bash
pip install opencv-python mediapipe
```

That's it — no GPU required.

---

## 🚀 Usage

```bash
python hand_tracker.py
```

- A window will open showing your webcam feed
- Hold your hand(s) in front of the camera
- Press **Q** to quit

---

## 🧠 How it works

MediaPipe detects **21 landmarks** on each hand. To figure out if a finger is up:

- **Index, Middle, Ring, Pinky** — if the fingertip landmark is *higher on screen* (smaller Y value) than the PIP joint below it, the finger is extended.
- **Thumb** — since the thumb moves sideways, we compare X coordinates instead, and flip the logic for left vs. right hand.

```
Finger extended  →  tip.y < pip.y
Thumb extended   →  tip.x < ip.x  (right hand)
                    tip.x > ip.x  (left hand)
```

---

## 📁 Project structure

```
hand-tracker/
│
├── hand_tracker.py   # Main script — run this
└── README.md
```

---

## 🔧 Tweaking it

Inside `hand_tracker.py` you can adjust these settings in the `mp_hands.Hands()` call:

| Parameter | Default | What it does |
|---|---|---|
| `max_num_hands` | `2` | Maximum hands to track at once |
| `min_detection_confidence` | `0.7` | How confident MediaPipe must be to detect a hand |
| `min_tracking_confidence` | `0.5` | How confident it must be to keep tracking |
| `model_complexity` | `0` | `0` = fast, `1` = more accurate |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| [OpenCV](https://opencv.org/) | Camera access and drawing |
| [MediaPipe](https://mediapipe.dev/) | Hand landmark detection |

---

## 📄 License

MIT — do whatever you want with it.