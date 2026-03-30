import React, { useEffect } from 'react';
import Layout, { Content, Header } from 'antd/es/layout/layout';
import Navbar from './components/navbar';
import { useLocation, useNavigate } from 'react-router-dom';
import Router from './router';
import { checkToken, validateToken } from './utils/checkToken';
import Draggable from 'react-draggable'
import './App.scss'
const App = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const needAuth = ['/course', '/teacher', '/admin', '/user'];

  useEffect(() => {
    const verifyCurrentToken = async () => {
      const hasToken = checkToken();
      const requiresAuth = needAuth.some((path) => pathname.startsWith(path));

      if (!hasToken && requiresAuth) {
        navigate('/login', { replace: true });
        return;
      }

      if (hasToken) {
        const isValid = await validateToken();
        if (!isValid && requiresAuth) {
          navigate('/login', { replace: true });
        }
      }
    };

    verifyCurrentToken();
  }, [navigate, pathname]);

  const headerStyle = {
    padding: "0",
    backgroundColor: "rgba(255, 255, 255, 0)",
    zIndex: "1000"
  }

  if (pathname === "/") {
    headerStyle.position = "fixed";
  }

  const handleButtonClick = () => {
    window.location.href = window.AIURL;
  }

  return (
    <Layout>
      <Header style={headerStyle}>
        <Navbar />
      </Header>
      <Layout>
        <Content style={{ minHeight: "92vh" }}>
          <Router />
        </Content>
        <Draggable bounds="parent" defaultPosition={{x: 1350, y:500}}>
          <button
              className="float-button"
              onClick={handleButtonClick}
            />
        </Draggable>
      </Layout>
    </Layout>
  );
}

export default App;
