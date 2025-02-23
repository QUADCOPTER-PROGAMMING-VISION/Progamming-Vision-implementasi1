import cv2

cap = cv2.VideoCapture(2)  # Ganti sesuai dengan device ID kamera
while True:
    ret, img = cap.read()
    if not ret:
        break  # Jika gagal membaca frame, keluar dari loop

    img = cv2.resize(img, (1000, 800))  # Kecilkan ukuran supaya cepat
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
