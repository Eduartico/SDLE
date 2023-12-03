import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./views/Login";
import Home from "./views/Home";
import List from "./views/List";
import Profile from "./views/Profile";
import Recipes from "./views/Recipes";

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/list/:listId" element={<List />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/recipes" element={<Recipes />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
