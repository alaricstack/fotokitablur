N=False
M=None
I='Foto Kita Blur Python'
H='='
B=print
import cv2 as A,numpy as f
J=M
K=M
E=M
try:import mediapipe as J;K=J.solutions.hands;E=J.solutions.drawing_utils;B('✅ MediaPipe solutions mode aktif')
except(AttributeError,ImportError)as U:B(f"❌ MediaPipe solutions error: {U}");B('\n'+H*60);B('  INSTALL MEDIAPIPE VERSI KOMPATIBEL:');B('  pip uninstall mediapipe -y');B('  pip install mediapipe==0.10.8');B(H*60);raise SystemExit(1)
V=51,51
W=5
O=K.Hands(static_image_mode=N,max_num_hands=1,min_detection_confidence=.7,min_tracking_confidence=.5)
P=A.VideoCapture(0)
F=N
L=0
D=True
Q=10,430
R=120,40
def X(hand_landmarks):
	A=hand_landmarks.landmark;E=[8,12,16,20];F=[5,9,13,17];B=[];J=A[0];C=A[4];D=A[5];G=((C.x-D.x)**2+(C.y-D.y)**2)**.5
	if G>.15:B.append(1)
	else:B.append(0)
	for(H,I)in zip(E,F):
		if A[H].y<A[I].y:B.append(1)
		else:B.append(0)
	return sum(B)
def Y(frame,kernel_size=V):return A.GaussianBlur(frame,kernel_size,0)
def Z(frame,blur_active,finger_count):C=blur_active;B=frame;D=B.copy();A.rectangle(D,(10,10),(400,100),(0,0,0),-1);A.addWeighted(D,.6,B,.4,0,B);E='BLUR: ON 'if C else'BLUR: OFF ';F=(0,0,255)if C else(0,255,0);A.putText(B,E,(20,50),A.FONT_HERSHEY_SIMPLEX,1,F,2);G=f"Jari: {finger_count}";A.putText(B,G,(20,85),A.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2);return B
def a(frame,ui_visible):
	D=frame;B,C=Q;E,F=R
	if ui_visible:G=50,150,50;H=255,255,255;I='UI: ON'
	else:G=80,80,80;H=200,200,200;I='UI: OFF'
	A.rectangle(D,(B,C),(B+E,C+F),G,-1);A.rectangle(D,(B,C),(B+E,C+F),(255,255,255),2);A.putText(D,I,(B+10,C+28),A.FONT_HERSHEY_SIMPLEX,.7,H,2);return D
def b(x,y):A,B=Q;C,D=R;return A<=x<=A+C and B<=y<=B+D
def c(event,x,y,flags,param):
	global D
	if event==A.EVENT_LBUTTONDOWN:
		if b(x,y):D=not D
A.namedWindow(I)
A.setMouseCallback(I,c)
B(H*50)
B('  GESTURE-CONTROLLED FULL CAMERA BLUR')
B('  2 Jari  = BLUR ON')
B('  Selain itu = BLUR OFF')
B('  Klik tombol kiri bawah untuk toggle UI')
B("  Tekan 'Q' untuk keluar")
B(H*50)
while True:
	d,C=P.read()
	if not d:B('Gagal ambil frame dari webcam!');break
	C=A.flip(C,1);e=A.cvtColor(C,A.COLOR_BGR2RGB);S=O.process(e);G=0
	if S.multi_hand_landmarks:
		for T in S.multi_hand_landmarks:
			if D:E.draw_landmarks(C,T,K.HAND_CONNECTIONS,E.DrawingSpec(color=(0,255,0),thickness=2),E.DrawingSpec(color=(255,0,0),thickness=2))
			G=X(T);L+=1
			if L>=W:F=G==2;L=0
	else:F=N;G=0
	if F:C=Y(C)
	if D:C=Z(C,F,G)
	C=a(C,D);A.imshow(I,C)
	if A.waitKey(1)&255==ord('q'):break
	if A.getWindowProperty(I,A.WND_PROP_VISIBLE)<1:break
P.release()
A.destroyAllWindows()
O.close()
B('Program selesai!')