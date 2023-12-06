import LineChart from "./LineChart";
import MQTTVideo from "./MQTTVideo";
import React, { useState, useEffect, useRef } from 'react';
import "../styles/Dashboard.css";
import { Col, Row, Card } from "antd";
import { Line } from 'react-chartjs-2';

const Dashboard = ({ socket }) => {
    const [videoSrc, setVideoSrc] = useState("");
    const [error, setError] = useState('No connection');
    const [heartRate, setHeartRate] = useState(0);
    const [heartKey, setHeartKey] = useState(0);
    const frameCount = useRef(0);
    const [frameRate, setFrameRate] = useState(0);
    const timeoutRef = useRef(null);
    const startTimeRef = useRef(null);

    useEffect(() => {
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
            };

            socket.onmessage = (message) => {
                clearTimeout(timeoutRef.current);
                const data = JSON.parse(message.data);
                if (data.type === 'video.update') {
                    if (data.frame) {
                        setVideoSrc('data:image/jpeg;base64,' + data.frame);
                        setError(null);
                        // updateWsHasData(true);
                        frameCount.current += 1;
                    } else {
                        setError('No data');
                    }
                } else if (data.type === 'video.hr') {
                    console.log(data.hr);
                    setHeartRate(data.hr);
                    setHeartKey(prevKey => prevKey + 1);
                }
            };
        }

        // Start the timer when the component mounts
        startTimeRef.current = Date.now();

        // Clear the timer when the component unmounts
        return () => {
            clearTimeout(timeoutRef.current);
            if (socket) {
                socket.close();
            }
        };
    }, [socket]);

    useEffect(() => {
        // Calculate the frame rate every second
        const timer = setInterval(() => {
            const currentTime = Date.now();
            const elapsedTime = currentTime - startTimeRef.current;
            const currentFrameRate = frameCount.current / (elapsedTime / 1000);
            setFrameRate(currentFrameRate.toFixed(2));
            console.log('Frame rate:', frameRate);
            console.log('Elapsed time:', elapsedTime);
            console.log('Frame count:', frameCount.current);
            console.log("currentFrameRate", currentFrameRate)

            frameCount.current = 0; // Reset frameCount


            startTimeRef.current = currentTime;
        }, 3000);

        // Clear the timer when the component unmounts
        return () => {
            clearInterval(timer);
        };
    }, []);

    return (
        <div style={{ height: '100%', width: '100%' }}>
            <Row style={{ height: '100%', width: '100%' }}>
                <Col span={12} style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                    <Row style={{ height: '70%', width: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                        <Card style={{ height: '98%', width: '98%' }}>
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', height: '95%' }}>
                                <MQTTVideo videoSrc={videoSrc} error={error} />
                            </div>
                        </Card>
                    </Row>
                    <Row style={{ height: '30%', width: '100%', minHeight: 0, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <Card style={{ height: '98%', width: '98%', minHeight: 0 }}>
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', height: '100%', width: '100%', minHeight: 0 }}>
                                <div style={{ height: '100%', width: '100%', minHeight: 0 }}>
                                    <LineChart heartRate={heartRate} />
                                </div>
                            </div>
                        </Card>
                    </Row>
                </Col>
                <Col span={12} style={{ height: '100%' }}>
                    <Row style={{ height: '30%' }}>
                        <Col span={12} style={{ height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <Card style={{ height: '95%', width: '95%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                                <h1>{heartRate}</h1>
                                <div className='heart' key={heartKey} style={{ opacity: 0.8 }}>
                                    ❤️
                                </div>
                            </Card>
                        </Col>
                        <Col span={12} style={{ height: '100%', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <div style={{ width: '95%', height: '95%', justifyContent: 'center', alignItems: 'center', display: 'flex' }}>
                                <Card style={{ width: '100%', height: '100%' }}>
                                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', height: '100%', width: '100%' }}>
                                        <Row style={{ width: '100%' }}>
                                            <Col span={12}>
                                                <h3>Frame Rate: </h3>
                                            </Col>
                                            <Col span={12}>
                                                <h3>{frameRate} FPS</h3>
                                            </Col>
                                        </Row>
                                        <Row style={{ width: '100%' }}>
                                            <Col span={12}>
                                                <h3>Latency:</h3>
                                            </Col>
                                            <Col span={12}>
                                                <h3>0 ms</h3>
                                            </Col>
                                        </Row>
                                    </div>
                                </Card>
                            </div>
                        </Col>
                    </Row>
                    <Row style={{ height: '70%', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                        <Card style={{ height: '98%', width: '98%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <Row justify="center" align="middle" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                                <Col span={24}>
                                    <Row justify="center" gutter={[16, 16]}>
                                        <Col span={24}>
                                            <div style={{ width: '100%' }}>
                                                <Line
                                                    data={{
                                                        labels: ['January', 'February', 'March', 'April', 'May'],
                                                        datasets: [
                                                            {
                                                                label: 'Data 1',
                                                                data: [12, 19, 3, 5, 2],
                                                                fill: false,
                                                                borderColor: 'rgb(255, 99, 132)',
                                                            },
                                                        ],
                                                    }}
                                                    options={{
                                                        responsive: true,
                                                        maintainAspectRatio: false,
                                                        scales: {
                                                            y: {
                                                                beginAtZero: true,
                                                            },
                                                        },
                                                    }}
                                                />
                                            </div>
                                        </Col>
                                    </Row>
                                    <Row justify="center" gutter={[16, 16]}>
                                        <Col span={24}>
                                            <div style={{ width: '100%' }}>
                                                <Line
                                                    data={{
                                                        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple'],
                                                        datasets: [
                                                            {
                                                                label: 'Data 2',
                                                                data: [5, 10, 15, 20, 25],
                                                                fill: false,
                                                                borderColor: 'rgb(54, 162, 235)',
                                                            },
                                                        ],
                                                    }}
                                                    options={{
                                                        responsive: true,
                                                        maintainAspectRatio: false,
                                                        scales: {
                                                            y: {
                                                                beginAtZero: true,
                                                            },
                                                        },
                                                    }}
                                                />
                                            </div>
                                        </Col>
                                    </Row>
                                    <Row justify="center" gutter={[16, 16]}>
                                        <Col span={24}>
                                            <div style={{ width: '100%' }}>
                                                <Line
                                                    data={{
                                                        labels: ['One', 'Two', 'Three', 'Four', 'Five'],
                                                        datasets: [
                                                            {
                                                                label: 'Data 3',
                                                                data: [7, 14, 21, 28, 35],
                                                                fill: false,
                                                                borderColor: 'rgb(75, 192, 192)',
                                                            },
                                                        ],
                                                    }}
                                                    options={{
                                                        responsive: true,
                                                        maintainAspectRatio: false,
                                                        scales: {
                                                            y: {
                                                                beginAtZero: true,
                                                            },
                                                        },
                                                    }}
                                                />
                                            </div>
                                        </Col>
                                    </Row>
                                </Col>
                            </Row>
                        </Card>
                    </Row>
                </Col>
            </Row>
        </div>
    );
};

export default Dashboard;