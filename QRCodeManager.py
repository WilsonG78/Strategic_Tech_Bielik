from pyzbar.pyzbar import decode
from PIL import Image
import io
import time
import os

class QRCodeManager:
    def __init__(self, picam2):
        self.picam2 = picam2
        self.running = False
        self.detected_codes = set()  # To keep track of already detected QR codes
        self.output_file = "QRCodes.txt"

        # Create the file if it doesn't exist
        if not os.path.exists(self.output_file):
            open(self.output_file, 'w').close()

    def detect_qr(self, image_data):
        image = Image.open(io.BytesIO(image_data))
        decoded_objects = decode(image)
        return [(obj.type, obj.data.decode("utf-8")) for obj in decoded_objects]

    def write_to_file(self, qr_data):
        """Write the QR code data to file if it's new"""
        with open(self.output_file, 'a') as f:  # 'a' mode for append
            f.write(qr_data + '\n')

    def working(self):
        self.running = True
        print("[QR] QRCodeManager started.")
        try:
            while self.running:
                # Capture a JPEG frame to memory
                stream = io.BytesIO()
                self.picam2.capture_file(stream, format="jpeg")
                frame_data = stream.getvalue()

                # Detect QR codes
                results = self.detect_qr(frame_data)
                if results:
                    for qr_type, qr_data in results:
                        if qr_data not in self.detected_codes:
                            print("[QR] New QR Code detected:", qr_data)
                            self.write_to_file(qr_data)
                            self.detected_codes.add(qr_data)  # Add to detected set
                        else:
                            print("[QR] Already detected QR Code:", qr_data)

                time.sleep(1 / 10)  # Adjust scanning frequency
        except Exception as e:
            print("[QR] Error:", e)
        finally:
            print("[QR] QRCodeManager stopped.")

    def stop(self):
        self.running = False
