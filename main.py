import numpy as np
import cv2, os, time

ADB_PATH = r"C:\ProgramData\chocolatey\lib\scrcpy\tools\adb.exe"
DEVICE_ID = "192.168.1.103:5555"   # <-- replace with your phone's ID

def adb(cmd):
    os.system(f'"{ADB_PATH}" -s {DEVICE_ID} {cmd}')

def swipe(x1, y1, x2, y2, dur=10):
    adb(f"shell input swipe {x1} {y1} {x2} {y2} {dur}")

# --- 1. Load and preprocess ---
img = cv2.imread(r"C:\Users\menen\Desktop\Importante\Proyectos\Instagram-Artist\simple_tiger.jpg",
                 cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Could not load the image")

# Resize to a convenient size
target_size = 600
h, w = img.shape
scale = target_size / max(h, w)
img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# Optional: slightly blur the image to reduce texture noise
img_blur = cv2.GaussianBlur(img, (5, 5), 0)

# Adaptive threshold with finer control
mask = cv2.adaptiveThreshold(
    img_blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    15, 5  # smaller window, smaller offset -> keeps detail
)

mask = cv2.bitwise_not(mask)

# Morphological cleanup
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# --- 3. Skeletonize (expects white lines on black background) ---
from skimage.morphology import skeletonize
skeleton = skeletonize(mask // 255)
skeleton = (skeleton * 255).astype("uint8")

cv2.imshow("skeleton", skeleton)
cv2.waitKey(0)
cv2.destroyAllWindows()

# --- 4. Extract contours ---
contours, _ = cv2.findContours(skeleton, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# --- 5. Map to phone screen ---
screen_w, screen_h = 1080, 2400
SCALE = 1.3
h, w = mask.shape
x0 = int((screen_w - w * SCALE) // 2)
y0 = int((screen_h - h * SCALE) // 2)

print("Switch to Instagram drawing canvas… starting in 3 s")
time.sleep(3)

# --- 4. Draw each contour smoothly ---
for c in contours:
    pts = c.squeeze()
    if len(pts.shape) != 2:
        continue
    pts = pts[::2]                 # take every 1st point for speed/smoothness
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        X1, Y1 = int(x0 + x1 * SCALE), int(y0 + y1 * SCALE)
        X2, Y2 = int(x0 + x2 * SCALE), int(y0 + y2 * SCALE)
        swipe(X1, Y1, X2, Y2, dur=8)

print("✅ Finished smooth contour drawing!")
