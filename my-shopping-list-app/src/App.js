import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./views/Login";
import Home from "./views/Home";
import List from "./views/List";
import Profile from "./views/Profile";
import Recipes from "./views/Recipes";
import Recipe from "./views/Recipe";

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<Home />} />
          <Route path="/list/:listId" element={<List />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/recipes" element={<Recipes />} />
          <Route path="/recipe/:recipeId" element={<Recipe />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
