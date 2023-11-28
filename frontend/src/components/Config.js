import React from 'react';
import { Select, Row, Col, Slider, Switch } from 'antd';
import { useState, useEffect } from 'react';
import MQTTVideo from './MQTTVideo';
import { debounce, set } from 'lodash';
import { sendApiRequest, sendSyncRequest } from '../api/api.js';
const Config = ({ socket }) => {
    const [resInput, setResInput] = useState(5);
    const [qualityInput, setQualityInput] = useState(8);
    const [brightnessInput, setBrightnessInput] = useState(0);
    const [contrastInput, setContrastInput] = useState(0);
    const [saturationInput, setSaturationInput] = useState(0);
    const [SEInput, setSEInput] = useState(0); // Special Effect
    const [awbInput, setAwbInput] = useState(1); // Auto White Balance
    const [awbGainInput, setAwbGainInput] = useState(1); // Auto White Balance Gain
    const [wbModeInput, setWbModeInput] = useState(0); // White Balance Mode
    const [aecInput, setAecInput] = useState(1); // Auto Exposure Control
    const [aecDSPInput, setAecDSPInput] = useState(1); // Auto Exposure Control DSP (aec2)
    const [aeLevelInput, setAeLevelInput] = useState(0); // Auto Exposure Level
    const [agcInput, setAgcInput] = useState(1); // Auto Gain Control
    const [gainCeilInput, setGainCeilInput] = useState(0); // Gain Ceiling
    const [bpcInput, setBpcInput] = useState(0); // Black Pixel Correction
    const [wpcInput, setWpcInput] = useState(1); // White Pixel Correction
    const [rawGMAInput, setRawGMAInput] = useState(1); // Raw Gamma Correction
    const [lencInput, setLencInput] = useState(1); // Lens Correction
    const [hmirrorInput, setHmirrorInput] = useState(0); // Horizontal Mirror
    const [vflipInput, setVflipInput] = useState(0); // Vertical Flip
    const [dcwInput, setDcwInput] = useState(1); // Defective Pixel Correction
    const [colorbarInput, setColorbarInput] = useState(0); // Color Bar
    const [ledIntensityInput, setLedIntensityInput] = useState(0); // LED Intensity
    const [wsHasData, setWsHasData] = useState(true);

    const [apiParam, setApiParam] = useState('');
    const [apiValue, setApiValue] = useState('');


    const handleFormSubmit = async () => {

        try {
            console.log(apiParam, apiValue);
            const data = await sendApiRequest(apiParam, apiValue);

            // Handle the API response
        } catch (error) {
            // Handle any errors
            console.error(error);
        }
    };

    const debouncedApiCall = debounce(handleFormSubmit, 1000);

    // this function syncs the config of camera from the ESP32 to the frontend
    const syncData = async () => {

        try {
            const data = await sendSyncRequest();
            console.log(data);

            // Handle the API response
        } catch (error) {
            // Handle any errors
            console.error(error);
        }
    };


    const updateWsHasData = (hasData) => {
        setWsHasData(hasData);
    }

    const onResChange = (value) => {
        console.log(`selected ${value}`);
        setResInput(value);
        setApiParam('framesize');
        setApiValue(value);
    };
    const onQualityChange = (value) => {
        console.log(`selected ${value}`);
        setQualityInput(value);
        setApiParam('quality');
        setApiValue(value);
    };

    const onBrightnessChange = (value) => {
        console.log(`selected ${value}`);
        setBrightnessInput(value);
        setApiParam('brightness');
        setApiValue(value);
    };

    const onContrastChange = (value) => {
        console.log(`selected ${value}`);
        setContrastInput(value);
        setApiParam('contrast');
        setApiValue(value);
    };

    const onSaturationChange = (value) => {
        console.log(`selected ${value}`);
        setSaturationInput(value);
        setApiParam('saturation');
        setApiValue(value);
    };

    const onSEChange = (value) => {
        console.log(`selected ${value}`);
        setSEInput(value);
        setApiParam('special_effect');
        setApiValue(value);
    }

    const onAwbChange = (value) => {
        console.log(`selected ${value}`);
        setAwbInput(value);
        setApiParam('awb');
        setApiValue(value);
    }

    const onAwbGainChange = (value) => {
        console.log(`selected ${value}`);
        setAwbGainInput(value);
        setApiParam('awb_gain');
        setApiValue(value);
    }

    const onWbModeChange = (value) => {
        console.log(`selected ${value}`);
        setWbModeInput(value);
        setApiParam('wb_mode');
        setApiValue(value);
    }

    const onAecChange = (value) => {
        console.log(`selected ${value}`);
        setAecInput(value);
        setApiParam('aec');
        setApiValue(value);
    }

    const onAecDSPChange = (value) => {
        console.log(`selected ${value}`);
        setAecDSPInput(value);
        setApiParam('aec2');
        setApiValue(value);
    }

    const onAeLevelChange = (value) => {
        console.log(`selected ${value}`);
        setAeLevelInput(value);
        setApiParam('ae_level');
        setApiValue(value);
    }

    const onAgcChange = (value) => {
        console.log(`selected ${value}`);
        setAgcInput(value);
        setApiParam('agc');
        setApiValue(value);
    }

    const onGainCeilChange = (value) => {
        console.log(`selected ${value}`);
        setGainCeilInput(value);
        setApiParam('gainceiling');
        setApiValue(value);
    }

    const onBpcChange = (value) => {
        console.log(`selected ${value}`);
        setBpcInput(value);
        setApiParam('bpc');
        setApiValue(value);
    }

    const onWpcChange = (value) => {
        console.log(`selected ${value}`);
        setWpcInput(value);
        setApiParam('wpc');
        setApiValue(value);
    }

    const onRawGMAChange = (value) => {
        console.log(`selected ${value}`);
        setRawGMAInput(value);
        setApiParam('raw_gma');
        setApiValue(value);
    }

    const onLencChange = (value) => {
        console.log(`selected ${value}`);
        setLencInput(value);
        setApiParam('lenc');
        setApiValue(value);
    }

    const onHmirrorChange = (value) => {
        console.log(`selected ${value}`);
        setHmirrorInput(value);
        setApiParam('hmirror');
        setApiValue(value);
    }

    const onVflipChange = (value) => {
        console.log(`selected ${value}`);
        setVflipInput(value);
        setApiParam('vflip');
        setApiValue(value);
    }

    const onDcwChange = (value) => {
        console.log(`selected ${value}`);
        setDcwInput(value);
        setApiParam('dcw');
        setApiValue(value);
    }

    const onColorbarChange = (value) => {
        console.log(`selected ${value}`);
        setColorbarInput(value);
        setApiParam('colorbar');
        setApiValue(value);
    }

    const onLedIntensityChange = (value) => {
        console.log(`selected ${value}`);
        setLedIntensityInput(value);
        setApiParam('led_intensity');
        setApiValue(value);
    }

    useEffect(() => {
        if (apiParam && apiValue)
            debouncedApiCall(); // Call the API when apiParam or apiValue changes
        return () => {
            debouncedApiCall.cancel();
        };
    }, [apiParam, apiValue]);

    useEffect(() => {
        syncData();
    }, []);

    if (wsHasData) {
        return (

            <div style={{ marginTop: '50px' }}>
                <Row gutter={16}>
                    <Col span={12}>
                        <Row gutter={16}>
                            <Col span={8}><h3>Camera resolution</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignContent: 'center' }}>
                                <Select
                                    defaultValue='5'
                                    style={{ width: 300, height: 40 }} // Increase width and height
                                    onChange={onResChange}
                                    options={[
                                        { value: '0', label: '96x96' },
                                        { value: '1', label: 'QQVGA(160x120)' },
                                        { value: '2', label: 'QCIF(176x144)' },
                                        { value: '3', label: 'HQVGA(240x176)' },
                                        { value: '4', label: '240x240' },
                                        { value: '5', label: 'QVGA(320x240)' },
                                        { value: '6', label: 'CIF(400x296)' },
                                        { value: '7', label: 'HVGA(480x320)' },
                                        { value: '8', label: 'VGA(640x480)' }
                                    ]}
                                />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>Camera quality</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>4</p>
                                    <Slider
                                        min={4}
                                        max={63}
                                        onChange={onQualityChange}
                                        value={typeof qualityInput === 'number' ? qualityInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>63</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>Brightness</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>-2</p>
                                    <Slider
                                        min={-2}
                                        max={2}
                                        onChange={onBrightnessChange}
                                        value={typeof brightnessInput === 'number' ? brightnessInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>2</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>Contrast</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>-2</p>
                                    <Slider
                                        min={-2}
                                        max={2}
                                        onChange={onContrastChange}
                                        value={typeof contrastInput === 'number' ? contrastInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>2</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>Saturation</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>-2</p>
                                    <Slider
                                        min={-2}
                                        max={2}
                                        onChange={onSaturationChange}
                                        value={typeof saturationInput === 'number' ? saturationInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>2</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>Special Effect</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Select
                                    defaultValue='0'
                                    style={{ width: 300, height: 40 }} // Increase width and height
                                    onChange={onSEChange}
                                    options={[
                                        { value: '0', label: 'No Effect' },
                                        { value: '1', label: 'Negative' },
                                        { value: '2', label: 'Grayscale' },
                                        { value: '3', label: 'Red Tint' },
                                        { value: '4', label: 'Green Tint' },
                                        { value: '5', label: 'Blue Tint' },
                                        { value: '6', label: 'Sepia' }
                                    ]}
                                />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>AWB</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onAwbChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>AWB Gain</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onAwbGainChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>WB Mode</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Select
                                    defaultValue='0'
                                    style={{ width: 300, height: 40 }} // Increase width and height
                                    onChange={onWbModeChange}
                                    options={[
                                        { value: '0', label: 'Auto' },
                                        { value: '1', label: 'Sunny' },
                                        { value: '2', label: 'Cloudy' },
                                        { value: '3', label: 'Office' },
                                        { value: '4', label: 'Home' }
                                    ]}
                                />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>AEC Sensor</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onAecChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>AEC DSP</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onAecDSPChange} />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>AE Level</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>-2</p>
                                    <Slider
                                        min={-2}
                                        max={2}
                                        onChange={onAeLevelChange}
                                        value={typeof aeLevelInput === 'number' ? aeLevelInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>2</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>AGC</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onAgcChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>Gain Ceiling</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>2x</p>
                                    <Slider
                                        min={0}
                                        max={6}
                                        onChange={onGainCeilChange}
                                        value={typeof gainCeilInput === 'number' ? gainCeilInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>128x</p>
                                </div>
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>BPC</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onBpcChange} />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>WPC</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onWpcChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>Raw GMA</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onRawGMAChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                                <h3>LENC</h3>
                            </Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onLencChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>HMirror</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onHmirrorChange} />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>VFlip</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onVflipChange} />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>DCW</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onDcwChange} defaultChecked />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8} style={{ display: 'flex', alignItems: 'center' }}><h3>Colorbar</h3></Col>
                            <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                                <Switch onChange={onColorbarChange} />
                            </Col>
                        </Row>
                        <Row gutter={16}>
                            <Col span={8}><h3>LED Intensity</h3></Col>
                            <Col span={16} style={{ display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
                                <div style={{ display: 'flex' }}>
                                    <p>0</p>
                                    <Slider
                                        min={0}
                                        max={255}
                                        onChange={onLedIntensityChange}
                                        value={typeof ledIntensityInput === 'number' ? ledIntensityInput : 0}
                                        style={{ width: 300, height: 40, marginLeft: '20px', marginRight: '20px' }} // Increase width and height
                                    />
                                    <p>255</p>
                                </div>
                            </Col>
                        </Row>
                    </Col>
                    <Col span={12}>
                        <MQTTVideo updateWsHasData={updateWsHasData} mode={2} socket={socket} />
                    </Col>
                </Row>
            </div>
        );
    }
    else {
        return (
            <h1>No data from ESP32!</h1>
        );
    }

};


export default Config;
