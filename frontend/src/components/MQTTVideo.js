import React, { useEffect, useState } from 'react';

function MQTTVideo() {
    const [videoSrc, setVideoSrc] = useState("");

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/video/');

        socket.onopen = () => {
            console.log('WebSocket Client Connected');
        };

        socket.onmessage = (message) => {
            const data = JSON.parse(message.data);
            if (data.type === 'video.update') {
                setVideoSrc('data:image/jpeg;base64,' + data.frame);
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
            <img src={videoSrc} style={{ position: 'absolute' }} width="640" height="480" alt="Video Stream" />
        </div>
    );
}

export default MQTTVideo;