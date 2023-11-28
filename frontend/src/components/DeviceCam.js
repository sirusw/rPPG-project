import React, { useEffect, useRef, useState } from 'react';
import LineChart from './LineChart';

function DeviceCam({socket}) {
    const videoRef = useRef();
    const mediaRecorderRef = useRef();
    const [error, setError] = useState(null);

    function arrayBufferToBase64(buffer) {
        let binary = '';
        let bytes = new Uint8Array(buffer);
        let len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    useEffect(() => {
        let socketOpened = false;
        const startRecording = () => {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    videoRef.current.srcObject = stream;
    
                    mediaRecorderRef.current = new MediaRecorder(stream);
                    mediaRecorderRef.current.ondataavailable = (event) => {
                        if (event.data && event.data.size > 0) {
                            const reader = new FileReader();
                            reader.readAsArrayBuffer(event.data);
                            reader.onloadend = function () {
                                const rawData = reader.result;
                                const base64Data = arrayBufferToBase64(rawData);
                                socket.send(base64Data);
                            }
                        }
                    };
                    mediaRecorderRef.current.start(10); // Start recording, and send data every 10 ms
                })
                .catch(err => {
                    console.log('Error accessing device camera: ', err);
                    setError('Cannot access device camera');
                });
        };
        if(socket != null){
            socket.onopen = () => {
                console.log('WebSocket Client Connected');
                socketOpened = true;
                startRecording();
            };
            socket.onclose = () => {
                socketOpened = false;
            };
            if (socket.readyState === WebSocket.OPEN) {
                startRecording();
            }
        }
    
        if (socket && socketOpened) {
            startRecording();
        }
    
        // Clean up the connection and stop the MediaRecorder when the component is unmounted
        return () => {
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
                mediaRecorderRef.current = null;
            }
            if (videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop());
                videoRef.current.srcObject = null;
            }
            console.log("DeviceCam unmounted");
        };
    }, [socket]);

    return (
        <div>
            {error ? (
                <div>{error}</div>
            ) : (
                <>
                    <video ref={videoRef} width="640" height="480" autoPlay />
                    <LineChart />
                </>
            )}
        </div>
    );
}

export default DeviceCam;