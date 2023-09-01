const video = document.getElementById('video');
const canvas = document.getElementById('virtualTryOnCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const socket = io.connect('http://localhost:5000'); // Update the URL if needed

let currentGlasses = 1; // Initialize with the default glasses image
const startVideo = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
};

startVideo();

socket.on('frame', (frame) => {
    const img = new Image();
    img.src = 'data:image/jpeg;base64,' + frame;
    img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
});
