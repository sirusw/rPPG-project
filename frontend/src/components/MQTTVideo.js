import React from 'react';

function MQTTVideo({ videoSrc, error }) {
  const height = '90%';
  const width = `calc(${height} * 3)`;
  return (
    <>
      {videoSrc && (
        <div style={{width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', alignContent:'center', justifySelf: 'center'}}>
          {(error === "No data" || error === "No connection") ? (
            <div>{error}</div>
          ) : (
            <>
              <img
                src={videoSrc}
                style={{ width: width, height: height }}
                alt="Video Stream"
              />
            </>
          )}
        </div>
      )}
    </>
  );
}

export default MQTTVideo;