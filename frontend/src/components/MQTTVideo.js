import React, { useEffect, useState } from 'react';

function MQTTVideo() {
    const [videoSrc, setVideoSrc] = useState("");
    const [error, setError] = useState('No connection');

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/video/');

        socket.onopen = () => {
            console.log('WebSocket Client Connected');
            setError('No data');
        };

        socket.onerror = (error) => {
            console.log('WebSocket Error: ', error);
            setError('No connection');
        };

        socket.onclose = (event) => {
            if (!event.wasClean) {
                setError('No connection');
            }
        };

        socket.onmessage = (message) => {
            const data = JSON.parse(message.data);
            if (data.type === 'video.update') {
                if (data.frame) {
                    setVideoSrc('data:image/jpeg;base64,' + data.frame);
                    setError(null); // Reset error when data is received
                } else {
                    setError('No data');
                }
            }
        };

        // Clean up the connection when the component is unmounted
        return () => {
            if(socket.readyState === WebSocket.OPEN) {
                socket.close();
            }
        };
    }, []);

    return (
        <div>
            {error ? (
                <div>{error}</div>
            ) : (
                <img src={videoSrc} style={{ position: 'absolute' }} width="640" height="480" alt="Video Stream" />
            )}
        </div>
    );
}

export default MQTTVideo;