import React, { useEffect, useState, useRef }
  from 'react';
import LineChart from './LineChart';
// mode: 1 for display, 2 for config
function MQTTVideo({ mode, updateWsHasData, socket }) {
  const [videoSrc, setVideoSrc] = useState("");
  const [error, setError] = useState('No connection');
  const timeoutRef = useRef(null);

  useEffect(() => {
    // const socket = new WebSocket('ws://localhost:8000/ws/video/');
    const timeoutDuration = 2000;

    if (socket) {
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
        // updateWsHasData(false);
      };

      socket.onmessage = (message) => {
        clearTimeout(timeoutRef.current);
        const data = JSON.parse(message.data);
        if (data.type === 'video.update') {
          if (data.frame) {
            setVideoSrc('data:image/jpeg;base64,' + data.frame);
            setError(null);
            updateWsHasData(true);
          } else {
            setError('No data');
            // updateWsHasData(false);
          }
        }
      };

      // timeoutRef.current = setTimeout(() => {
      //   setError('No data');
      //   // updateWsHasData(false);
      // }, timeoutDuration);

    }


    // return () => {
    //   clearTimeout(timeoutRef.current);
    //   if (socket.readyState === WebSocket.OPEN) {
    //     socket.close();
    //   }
    // };

  }, [socket]);



  return (
    <>
      <div>
        {(error === "No data" || error === "No connection") ? (<div>{error}</ div>) :
          (<><img src={videoSrc} width="640" height="480" alt="Video Stream" />
            {mode === 1 ? <LineChart /> : ""}

          </>)
        }
      </ div>

    </>
  );
}

export default MQTTVideo;