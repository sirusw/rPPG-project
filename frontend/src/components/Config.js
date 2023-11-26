import React from 'react';
import { Select, Row, Col, Slider, Switch } from 'antd';
import { useState } from 'react';
import MQTTVideo from './MQTTVideo';
const Config = () => {
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

    const onResChange = (value) => {
        console.log(`selected ${value}`);
        setResInput(value);
    };
    const onQualityChange = (value) => {
        console.log(`selected ${value}`);
        setQualityInput(value);
    };

    const onBrightnessChange = (value) => {
        console.log(`selected ${value}`);
        setBrightnessInput(value);
    };

    const onContrastChange = (value) => {
        console.log(`selected ${value}`);
        setContrastInput(value);
    };

    const onSaturationChange = (value) => {
        console.log(`selected ${value}`);
        setSaturationInput(value);
    };

    const onSEChange = (value) => {
        console.log(`selected ${value}`);
        setSEInput(value);
    }

    const onAwbChange = (value) => {
        console.log(`selected ${value}`);
        setAwbInput(value);
    }

    const onAwbGainChange = (value) => {
        console.log(`selected ${value}`);
        setAwbGainInput(value);
    }

    const onWbModeChange = (value) => {
        console.log(`selected ${value}`);
        setWbModeInput(value);
    }

    const onAecChange = (value) => {
        console.log(`selected ${value}`);
        setAecInput(value);
    }   

    const onAecDSPChange = (value) => {
        console.log(`selected ${value}`);
        setAecDSPInput(value);
    }

    const onAeLevelChange = (value) => {
        console.log(`selected ${value}`);
        setAeLevelInput(value);
    }

    const onAgcChange = (value) => {
        console.log(`selected ${value}`);
        setAgcInput(value);
    }

    const onGainCeilChange = (value) => {
        console.log(`selected ${value}`);
        setGainCeilInput(value);
    }

    const onBpcChange = (value) => {
        console.log(`selected ${value}`);
        setBpcInput(value);
    }

    const onWpcChange = (value) => {
        console.log(`selected ${value}`);
        setWpcInput(value);
    }

    const onRawGMAChange = (value) => {
        console.log(`selected ${value}`);
        setRawGMAInput(value);
    }

    const onLencChange = (value) => {
        console.log(`selected ${value}`);
        setLencInput(value);
    }

    const onHmirrorChange = (value) => {
        console.log(`selected ${value}`);
        setHmirrorInput(value);
    }

    const onVflipChange = (value) => {
        console.log(`selected ${value}`);
        setVflipInput(value);
    }

    const onDcwChange = (value) => {
        console.log(`selected ${value}`);
        setDcwInput(value);
    }

    const onColorbarChange = (value) => {
        console.log(`selected ${value}`);
        setColorbarInput(value);
    }  

    const onLedIntensityChange = (value) => {
        console.log(`selected ${value}`);
        setLedIntensityInput(value);
    }
    
    return (
        <div style={{marginTop: '50px'}}>
            <Row gutter={16}>
  <Col span={12}>
            <Row gutter={16}>
                <Col span={8}><h3>Camera resolution</h3></Col>
                <Col span={16} style={{display: 'flex', alignContent: 'center'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
                    <Switch onChange={onRawGMAChange} defaultChecked/>
                </Col>
            </Row>
            <Row gutter={16}>
                <Col span={8} style={{ display: 'flex', alignItems: 'center' }}>
                    <h3>LENC</h3>
                </Col>
                <Col span={16} style={{ display: 'flex', alignItems: 'center' }}>
                    <Switch onChange={onLencChange} defaultChecked/>
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
                    <Switch onChange={onDcwChange} defaultChecked/>
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
                <Col span={16} style={{display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <div style={{ display: 'flex'}}>
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
    <MQTTVideo />
  </Col>
</Row>
        </div>
    );
};


export default Config;
