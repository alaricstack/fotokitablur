"""
Gesture-Controlled Full Camera Blur
Pose ✌️ (2 jari) = BLUR ON
Pose 👊 (0 jari) atau 🖐️ (5 jari) = BLUR OFF
"""

import cv2
import numpy as np

# ============ FIX IMPORT MEDIAPIPE - AUTO DETECT VERSION ============
mp = None
mp_hands = None
mp_drawing = None

try:
    import mediapipe as mp
    # Coba akses solutions (versi lama 0.8.x - 0.10.x)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    print("✅ MediaPipe solutions mode aktif")
except (AttributeError, ImportError) as e:
    print(f"❌ MediaPipe solutions error: {e}")
    print("\n" + "="*60)
    print("  INSTALL MEDIAPIPE VERSI KOMPATIBEL:")
    print("  pip uninstall mediapipe -y")
    print("  pip install mediapipe==0.10.8")
    print("="*60)
    raise SystemExit(1)

# ============ KONFIGURASI ============
BLUR_KERNEL = (51, 51)          # Ukuran blur (harus ganjil)
COOLDOWN_FRAMES = 5             # Delay biar gak flicker

# ============ INISIALISASI ============
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
cap = cv2.VideoCapture(0)

# State
blur_active = False
cooldown_counter = 0
ui_visible = True        # Default UI aktif

# Tombol toggle
BUTTON_POS = (10, 430)   # Kiri bawah
BUTTON_SIZE = (120, 40)  # Lebar, Tinggi


def count_fingers(hand_landmarks):
    """
    Hitung jumlah jari terangkat.
    Returns: 0-5 (jumlah jari terangkat)
    """
    landmarks = hand_landmarks.landmark

    TIP_IDS = [8, 12, 16, 20]   # Index, Middle, Ring, Pinky
    MCP_IDS = [5, 9, 13, 17]    # Knuckle masing-masing jari

    fingers = []

    # Jempol: cek distance dari thumb tip ke index finger base
    # Kalau jempol closed/sembunyi, jaraknya deket
    # Kalau jempol naik, jaraknya jauh
    wrist = landmarks[0]
    thumb_tip = landmarks[4]
    index_base = landmarks[5]

    # Hitung distance thumb tip ke index base
    dist_thumb_index = ((thumb_tip.x - index_base.x)**2 + (thumb_tip.y - index_base.y)**2)**0.5

    # Threshold: kalau distance > 0.15 berarti jempol terbuka/naik
    if dist_thumb_index > 0.15:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 jari lainnya (cek y-coordinate)
    for tip_id, mcp_id in zip(TIP_IDS, MCP_IDS):
        if landmarks[tip_id].y < landmarks[mcp_id].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


def apply_full_blur(frame, kernel_size=BLUR_KERNEL):
    """
    Blur seluruh frame pakai Gaussian Blur
    """
    return cv2.GaussianBlur(frame, kernel_size, 0)


def draw_status(frame, blur_active, finger_count):
    """
    Gambar status di frame (pojok kiri atas)
    """
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (400, 100), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    status_text = "BLUR: ON " if blur_active else "BLUR: OFF "
    status_color = (0, 0, 255) if blur_active else (0, 255, 0)
    cv2.putText(frame, status_text, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

    finger_text = f"Jari: {finger_count}"
    cv2.putText(frame, finger_text, (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, "2 Jari = BLUR ON | Selain itu = OFF", (10, frame.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    return frame


def draw_button(frame, ui_visible):
    """
    Gambar tombol toggle UI di pojok kiri bawah
    """
    bx, by = BUTTON_POS
    bw, bh = BUTTON_SIZE

    # Background tombol
    if ui_visible:
        btn_color = (50, 150, 50)  # Hijau = ON
        text_color = (255, 255, 255)
        btn_text = "UI: ON"
    else:
        btn_color = (80, 80, 80)   # Abu = OFF
        text_color = (200, 200, 200)
        btn_text = "UI: OFF"

    # Kotak tombol
    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), btn_color, -1)
    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 255, 255), 2)

    # Teks tombol
    cv2.putText(frame, btn_text, (bx + 10, by + 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    return frame


def is_click_on_button(x, y):
    """
    Cek apakah koordinat click ada di tombol
    """
    bx, by = BUTTON_POS
    bw, bh = BUTTON_SIZE
    return bx <= x <= bx + bw and by <= y <= by + bh


# ============ CALLBACK MOUSE ============
def mouse_callback(event, x, y, flags, param):
    global ui_visible
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_click_on_button(x, y):
            ui_visible = not ui_visible


cv2.namedWindow('Gesture Face Blur')
cv2.setMouseCallback('Gesture Face Blur', mouse_callback)

# ============ MAIN LOOP ============
print("=" * 50)
print("  GESTURE-CONTROLLED FULL CAMERA BLUR")
print("  2 Jari  = BLUR ON")
print("  Selain itu = BLUR OFF")
print("  Klik tombol kiri bawah untuk toggle UI")
print("  Tekan 'Q' untuk keluar")
print("=" * 50)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal ambil frame dari webcam!")
        break

    frame = cv2.flip(frame, 1)

    # Deteksi tangan
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar hand landmarks hanya kalau UI aktif
            if ui_visible:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

            finger_count = count_fingers(hand_landmarks)

            cooldown_counter += 1
            if cooldown_counter >= COOLDOWN_FRAMES:
                # 2 jari = blur ON, selain itu = blur OFF
                blur_active = (finger_count == 2)
                cooldown_counter = 0
    else:
        # Ga ada tangan = 0 jari = blur OFF
        blur_active = False
        finger_count = 0

    if blur_active:
        frame = apply_full_blur(frame)

    # Gambar UI hanya kalau ui_visible = True
    if ui_visible:
        frame = draw_status(frame, blur_active, finger_count)

    # Tombol toggle selalu digambar
    frame = draw_button(frame, ui_visible)

    cv2.imshow('Gesture Face Blur', frame)

    # Cek kalau window ditutup (klik X) atau tekan Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Cek kalau window visibility = 0 (ditutup pake X)
    if cv2.getWindowProperty('Gesture Face Blur', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("Program selesai!")