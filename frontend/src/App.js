import React from 'react';
import { useState } from 'react';
import {
  DesktopOutlined, SettingOutlined 
} from '@ant-design/icons';
import { Select, Layout, Menu, theme, Typography } from 'antd';
import MQTTVideo from './components/MQTTVideo';
import Config from './components/Config';
import DeviceCam from './components/DeviceCam';
import LineChart from './components/LineChart';
const { Header, Content, Footer } = Layout;


function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
}
const items = [
  getItem('Dashboard', '1', <DesktopOutlined />),
  getItem('Configuration', '2', <SettingOutlined />)
];

const App = () => {
  const [selectedKey, setSelectedKey] = useState('1');
  const [camera, setCamera] = useState('device');
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  let content;

  if(selectedKey === '1') {
    content = 
    <div style={{height: '100%'}}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Typography>
          <h3>Camera selection:</h3>
        </Typography>
        <Select
          defaultValue="device"
          style={{ width: 180, marginLeft: 10 }}
          onChange={(value) => setCamera(value)}
          options={[
            {
              value: 'device',
              label: 'Device Camera',
            },
            {
              value: 'esp32',
              label: 'Esp32 Camera',
            },
          ]}
        />
      </div>
      {camera === 'device' ? <DeviceCam /> : <MQTTVideo />}
      <LineChart/>
      </div>;
  } else if(selectedKey === '2') {
    content = <Config />;
  }

  return (
    <Layout className="layout" style={{height: '100%'}}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          flex: '0 0 auto'
        }}
      >
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['1']}
          disabledOverflow={true}
          style={{height: 'auto', overflow: 'auto'}}
          items={items}
          onClick={(e) => setSelectedKey(e.key)}
        />
      </Header>
      <Content
        style={{
          padding: '0 50px',
          overflow: 'auto',
          flex: '1 0 auto',
          minHeight: 'calc(100vh - 150px)',
          display: 'flex',
        }}
      >
          {content}
      </Content>
      <Footer
        style={{
          display: 'flex',
          textAlign: 'center',
          justifyContent: 'center',
          height: '5vh',
          flex: '0 0 auto',
          backgroundColor: colorBgContainer
        }}
      >
        <p style={{
          justifyContent: 'center',
          display: 'flex',
          alignItems: 'center'}}>
            @2023 Created by Team 11 from COMP7310, HKU
          </p>
      </Footer>
    </Layout>
  );
};
export default App;