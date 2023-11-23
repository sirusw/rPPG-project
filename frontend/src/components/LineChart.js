import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, LineElement, PointElement, LineController } from 'chart.js';

Chart.register(CategoryScale, LinearScale, LineElement, PointElement, LineController);

const LineChart = () => {
  const [dataPoints, setDataPoints] = useState([]);

  // Function to add data
  const addDataPoint = (data) => {
    setDataPoints(prevDataPoints => {
      if (prevDataPoints.length >= 10) {
        return [data]; // Reset the data array when it reaches 11 points
      } else {
        return [...prevDataPoints, data];
      }
    });
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      addDataPoint(Math.floor(Math.random() * 40) + 60);
    }, 3000);

    return () => clearInterval(intervalId); // Clean up on unmount
  }, []);

  const data = {
    labels: Array.from({ length: 10 }, (_, i) => i + 1), // labels are always 1 to 10
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
  };

  return (
    <div style={{ width: '640px', height: '480px', marginTop: '100px', marginLeft: '50px'}}>
      <Line data={data} options={options} />
    </div>
  );
};

export default LineChart;