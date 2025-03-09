import cv2
from pyzbar.pyzbar import decode


def read_qr_from_video():
    cap = cv2.VideoCapture(0)  # Open default camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        qr_codes = decode(frame)
        for qr in qr_codes:
            data = qr.data.decode('utf-8')
            x, y, w, h = qr.rect

            # Draw a rectangle around QR code
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Display decoded text
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    read_qr_from_video()
