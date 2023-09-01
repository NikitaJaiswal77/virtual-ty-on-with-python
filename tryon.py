from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

glasses_overlay = None  

@app.route('/')
def upload():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    global glasses_overlay

    if request.method == 'POST':
        f = request.files['file']
        uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(uploaded_path)
        
        # Load the uploaded image using OpenCV
        glasses_overlay = cv2.imread(uploaded_path, cv2.IMREAD_UNCHANGED)

    return redirect(url_for('tryon'))

@app.route('/tryon', methods=['GET'])
def tryon():
    if glasses_overlay is None:
        return "Please upload an image first."

    cap = cv2.VideoCapture(0)  # Open webcam
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_scale, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            overlay_resize = cv2.resize(glasses_overlay, (w, int(h * 0.8)))

            for i in range(overlay_resize.shape[0]):
                for j in range(overlay_resize.shape[1]):
                    if overlay_resize[i, j, 3] != 0:  # Check the alpha channel
                        frame[y + i, x + j, :3] = overlay_resize[i, j, :3]  # Overlay glasses image

        cv2.imshow('Virtual Try-On', frame)

        if cv2.waitKey(10) == ord('e'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Virtual try-on completed."


if __name__ == '__main__':
    app.run(debug=True)
