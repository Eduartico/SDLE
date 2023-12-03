import React from 'react';
import { Link } from 'react-router-dom';

const BottomAppBar = () => {
  return (
    <div className="bottom-app-bar">
      <Link to="/home">Home</Link>
      <Link to="/lists">Lists</Link>
      <Link to="/profile">Profile</Link>
    </div>
  );
};

export default BottomAppBar;