#!/usr/bin/python3
from flask import Flask, Response
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import io
import time
import threading

from QRCodeManager import QRCodeManager


class CameraManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.picam2 = Picamera2()
        self.app.add_url_rule("/video", "video_feed", self.video_feed)

        self.qr_manager = QRCodeManager(self.picam2)
        self.qr_thread = threading.Thread(target=self.qr_manager.working, daemon=True)
    def generate_frames(self):
        # Configure video capture
        video_config = self.picam2.create_video_configuration(main={"size": (640, 480)})
        self.picam2.configure(video_config)

        # Create an in-memory stream
        stream = io.BytesIO()

        # Start the camera
        self.picam2.start()
        self.qr_thread.start()


        try:
            while True:
                # Capture to the in-memory stream
                stream.seek(0)
                self.picam2.capture_file(stream, format="jpeg")
                stream.seek(0)

                # Yield the frame in the multipart format
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n"
                )

                # Clear the stream for the next frame
                stream.seek(0)
                stream.truncate()

                # Small delay to control frame rate
                time.sleep(1 / 24)
        finally:
            self.picam2.stop()
            self.qr_manager.stop()

    def video_feed(self):
        return Response(
            self.generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    def working(self):
        self.app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    camera = CameraManager()
    camera.working()
