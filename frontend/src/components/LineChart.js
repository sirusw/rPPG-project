import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, LineElement, PointElement, LineController } from 'chart.js';

Chart.register(CategoryScale, LinearScale, LineElement, PointElement, LineController);

const LineChart = ({ heartRate }) => {
  const [dataPoints, setDataPoints] = useState([]);

  // Function to add data
  const addDataPoint = (data) => {
    setDataPoints(prevDataPoints => {
      if (prevDataPoints.length >= 20) {
        return [data]; // Reset the data array when it reaches 11 points
      } else {
        return [...prevDataPoints, data];
      }
    });
  };

  useEffect(() => {
    addDataPoint(heartRate);
  }, [heartRate]);

  const data = {
    labels: Array.from({ length: 20 }, (_, i) => i + 1), // labels are always 1 to 10
    datasets: [
      {
        label: 'Heart Rate',
        data: dataPoints,
        fill: false,
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgba(255, 99, 132, 0.2)',
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        type: 'linear',
        beginAtZero: true,
      },
    },
    maintainAspectRatio: false
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%' }}>
      <div style={{ flex: '1 1 auto', overflow: 'auto' }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default LineChart;