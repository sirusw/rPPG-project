import React, { useEffect, useRef, useState } from 'react';

function DeviceCam() {
    const videoRef = useRef();
    const mediaRecorderRef = useRef();
    const [error, setError] = useState(null);

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/video/');

        socket.onopen = () => {
            console.log('WebSocket Client Connected');
            startRecording();
        };

        const startRecording = () => {
            navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoRef.current.srcObject = stream;

                mediaRecorderRef.current = new MediaRecorder(stream);
                mediaRecorderRef.current.ondataavailable = (event) => {
                    if (event.data && event.data.size > 0) {
                        socket.send(event.data);
                    }
                };
                mediaRecorderRef.current.start(10); // Start recording, and send data every 10 ms
            })
            .catch(err => {
                console.log('Error accessing device camera: ', err);
                setError('Cannot access device camera');
            });
        };

        // Clean up the connection and stop the MediaRecorder when the component is unmounted
        return () => {
            if(socket.readyState === WebSocket.OPEN) {
                socket.close();
            }
            if(mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
            }
            if(videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    return (
        <div>
            {error ? (
                <div>{error}</div>
            ) : (
                <video ref={videoRef} style={{ position: 'absolute' }} width="640" height="480" autoPlay />
            )}
        </div>
    );
}

export default DeviceCam;