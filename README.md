# 📷 Foto Kita Blur - Gesture-Controlled Camera Blur

Aplikasi blur kamera real-time dengan kontrol gesture tangan menggunakan MediaPipe.

## 🎮 Cara Kerja

- ✌️ **Pose 2 Jari** → **BLUR ON** (kamera langsung blur seluruh layar)
- **Pose Lainnya** (0, 1, 3, 4, 5 jari) → **BLUR OFF** (kamera normal)
- **Tombol UI Toggle** → Sembunyikan/tampilkan overlay UI

## 🚀 Instalasi

### 1. Install Python
Pastikan Python 3.8+ sudah terinstall. Download di [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
```bash
pip install opencv-python numpy mediapipe==0.10.8
```

Atau kalau mau lebih spesifik:
```bash
pip install opencv-python==4.8.0.76
pip install numpy==1.24.3
pip install mediapipe==0.10.8
```

### 3. Jalankan Program
```bash
python fotokitablur.py
```

## 📋 Requirements

| Package | Versi | Deskripsi |
|---------|-------|-----------|
| `opencv-python` | 4.8.x | Untuk capture webcam dan image processing |
| `numpy` | 1.24.x | Manipulasi array untuk OpenCV |
| `mediapipe` | 0.10.8 | Deteksi tangan dan landmark (WAJIB versi ini!) |

## ⚠️ Catatan Penting

- **MediaPipe versi 0.10.8 sangat penting!** Versi lain mungkin tidak kompatibel dengan kode ini.
- Pastikan webcam/ kamera ter-connect dan bisa dipakai.
- Kalau ada error `ModuleNotFoundError`, cek lagi instalasi packages di atas.

## 🎯 Fitur

- ✅ Blur seluruh kamera real-time
- ✅ Deteksi gesture tangan (0-5 jari)
- ✅ Toggle UI on/off dengan klik tombol
- ✅ Support tangan kiri dan kanan
- ✅ Cooldown mechanism untuk mencegah flicker
- ✅ UI overlay dengan status dan info

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'mediapipe'`
```bash
pip install mediapipe==0.10.8
```

### Error: `ModuleNotFoundError: No module named 'cv2'`
```bash
pip install opencv-python
```

### Error: `Could not open video capture`
- Cek apakah webcam sedang dipakai aplikasi lain
- Coba restart program

### MediaPipe error / webcam freeze
```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.8
```

## 📁 Struktur File

```
Foto Kita Blur/
├── fotokitablur.py      # Main program
└── README.md            # Dokumentasi
```

## 👤 Credits

Dibuat dengan ❤️ menggunakan Python, OpenCV, dan MediaPipe.
