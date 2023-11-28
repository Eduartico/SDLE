import React, { createContext, useContext, useState } from 'react';
import ApiService from '../services/ApiService';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const login = async (username, password) => {
    try {
      const response = await ApiService.authenticateUser(username, password);
      setUser(response.data.user);
      
      navigate('/'); // Use navigate to redirect to the home page
    } catch (error) {
      console.error('Authentication failed:', error);
      navigate('/login');
    }
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
