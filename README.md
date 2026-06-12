# 🎭 Mood Detection with GIF Overlay

A real-time computer vision project that detects your **facial expressions** and **hand gestures** via webcam and overlays a matching GIF on the camera feed.

---

## 📸 Demo

| Mood | Trigger | GIF Shown |
|---|---|---|
| 👍 THUMBS_UP | Thumb up, other fingers curled | `thumbsup_3.jpg` |
| ☝️ YOU | Index finger pointing, thumb down | `you_3.jpg` |
| 😄 HAPPY | Slight smile (mouth slightly open + wide) | `happy_1.jpg` |
| 😱 SCARY | Mouth wide open | *(no GIF, text only)* |
| 😐 NEUTRAL | No gesture or expression detected | *(no GIF, text only)* |

---

## 🗂️ Project Structure

```
your_project/
│
├── main.py              ← Main script
│
└── gifs/
    ├── happy_1.jpg
    ├── thumbsup_3.jpg
    └── you_3.jpg
```

---

## ⚙️ Requirements

- Python 3.8+
- Webcam

### Install Dependencies

```bash
pip install opencv-python mediapipe Pillow numpy
```

---

## 🚀 How to Run

```bash
python main.py
```

Press **`Q`** to quit the camera window.

---

## 🧠 How It Works

### 1. Hand Gesture Detection
Uses **MediaPipe Hands** to track 21 hand landmarks per frame.

| Gesture | Logic |
|---|---|
| THUMBS_UP | `thumb_tip.y < thumb_ip.y` AND index/middle fingers curled |
| YOU | `index_tip.y < index_pip.y` AND middle curled AND thumb down |

> Y-axis in image coordinates increases **downward**, so a lower `.y` value means higher on screen.

### 2. Face Expression Detection
Uses **MediaPipe FaceMesh** with 468 landmarks. Key points used:

| Landmark Index | Point |
|---|---|
| 13 | Upper lip |
| 14 | Lower lip |
| 61 | Mouth left corner |
| 291 | Mouth right corner |

**Logic:**
- `mouth_opening > 0.05` → **SCARY**
- `0.015 < mouth_opening < 0.05` AND `mouth_width > 0.06` → **HAPPY**

### 3. GIF Overlay
- GIFs/images are loaded once at startup using **Pillow** into a list of BGR NumPy arrays
- Each frame, the correct image is resized to `150×150` and pasted onto the **bottom-right corner** of the camera feed using `overlay_gif()`

---

## 🔧 Customization

### Change GIF Size
In `main.py`, find this line and adjust `size`:
```python
overlay_gif(frame, gif_frame, position=(w - 170, h - 170), size=(150, 150))
```

### Change GIF Position
| Position | Code |
|---|---|
| Bottom-right | `position=(w - 170, h - 170)` |
| Top-left | `position=(20, 80)` |
| Top-right | `position=(w - 170, 20)` |
| Bottom-left | `position=(20, h - 170)` |

### Add a New Mood
1. Add your GIF to the `gifs/` folder
2. Add it to `gif_map` in `main.py`:
```python
gif_map = {
    "HAPPY":     load_gif("gifs/happy_1.jpg"),
    "THUMBS_UP": load_gif("gifs/thumbsup_3.jpg"),
    "YOU":       load_gif("gifs/you_3.jpg"),
    "WINK":      load_gif("gifs/wink.gif"),   # ← new mood
}
```
3. Add detection logic in the camera loop

---

## 🐛 Common Issues

| Problem | Fix |
|---|---|
| `FileNotFoundError` for GIF | Make sure the `gifs/` folder is in the **same directory** as `main.py` |
| Black box instead of image | Check file path and confirm the image opens correctly in an image viewer |
| Camera not opening | Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if you have multiple cameras |
| Laggy feed | Reduce GIF `size` to `(100, 100)` for better performance |
| Gesture not detecting | Ensure good lighting and keep hand clearly visible in frame |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| `opencv-python` | Camera capture, image drawing, display |
| `mediapipe` | Face mesh + hand landmark detection |
| `Pillow` | Loading and parsing GIF frames |
| `numpy` | Array conversion between Pillow and OpenCV |
| `math` | Calculating mouth width with `hypot` |

---
