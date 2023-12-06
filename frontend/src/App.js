import React, { useEffect } from 'react';
import { useState } from 'react';
import {
  DesktopOutlined, SettingOutlined, MenuOutlined
} from '@ant-design/icons';
import { Select, Layout, Menu, theme, Button } from 'antd';
import Dashboard from './components/Dashboard';
import Config from './components/Config';
import { setCsrfToken } from './api/api';
const { Header, Content, Footer, Sider } = Layout;

const contentStyle = {
  textAlign: 'center',
  minHeight: 120,
  lineHeight: '120px',
  color: '#fff',
  backgroundColor: '#108ee9',
};

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
  const [camera, setCamera] = useState('esp32');
  const [wsHasData, setWsHasData] = useState(true);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    if (!socket) {
      const socketConnection = new WebSocket('ws://localhost:8000/ws/video/');
      setSocket(socketConnection);
    }
  }
    , []);

  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const updateWsHasData = (hasData) => {
    setWsHasData(hasData);
  }

  useEffect(() => {
    setCsrfToken()
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
  }, []);

  useEffect(() => {
    setCamera('device');
  }
    , [selectedKey]);

  return (
    <Layout className="layout" style={{ height: '100vh' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          flex: '0 0 auto'
        }}
      >
        <div className="demo-logo" />
        {/* <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['1']}
          disabledOverflow={true}
          style={{ height: 'auto', overflow: 'auto' }}
          items={items}
          onClick={(e) => setSelectedKey(e.key)}
        /> */}
        <h1 style={{ fontFamily: 'Hedvig Letters Serif, serif', color: 'white' }}>Real-Time rPPG-based Heart Rate Monitoring Dashboard</h1>
      </Header>
      <Content
        className="site-layout"
        style={{
          padding: '0 50px',
          minHeight: 'calc(100vh - 200px)',
          width: '100%',
          height: '100%',
          textAlign: 'center',
        }}
      >
        <Layout style={{ padding: '15px 0', height: '100%', width: '100%' }}>
          <Sider
            style={{
              background: colorBgContainer,
              borderRight: '1px solid #e8e8e8',
              alignContent: 'center',
              alignItems: 'center',
              overflowY: 'auto',
              overflowX: 'hidden',
              height: '100%',
              position: 'relative'
            }}
            width={'22%'}>
            <Config />
          </Sider>
          <div style={{ height: '100%', width: '100%' }}>
            <Dashboard socket={socket} />
          </div>
        </Layout>
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
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto'
        }}>
          @2023 Created by Team 11 from COMP7310, HKU
        </p>
      </Footer>
    </Layout>
  );
};
export default App;