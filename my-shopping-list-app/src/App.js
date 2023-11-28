import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './views/Login';
import Home from './views/Home';
import List from './views/List';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/list/:listId" element={<List/>} /> 
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
