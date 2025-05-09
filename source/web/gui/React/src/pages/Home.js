import React from 'react';
import '../styles/Home.css';
import UrlInputBox from '../components/UrlInputBox';

function Home() {
  return (
    <div className="home-container">
      <div className="top-buttons">
        <button className="btn white">Search</button>
        <button className="btn black">About</button>
      </div>
      <div className="center-content">
        <h1 className="title"> 피싱 탐지 시스템</h1>
        <UrlInputBox />
      </div>
    </div>
  );
}

export default Home;
