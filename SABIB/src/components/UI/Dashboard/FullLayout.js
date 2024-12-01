// FullLayout.js

import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { Container } from 'reactstrap';
import { Outlet } from 'react-router-dom';

const FullLayout = () => {
  return (
    <main>
      <div className="pageWrapper d-lg-flex">
        {/* Sidebar */}
        <aside className="sidebarArea shadow" id="sidebarArea">
          <Sidebar />
        </aside>
        {/* Content Area */}
        <div className="contentArea">
          {/* Header */}
          <Header />
          {/* Middle Content */}
          <Container className="p-4 wrapper" fluid>
            <Outlet /> {/* Renders nested routes */}
          </Container>
        </div>
      </div>
    </main>
  );
};

export default FullLayout;
