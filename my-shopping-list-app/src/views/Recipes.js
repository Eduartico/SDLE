import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ApiService from "../services/ApiService";
import { Button, ListGroup, Modal } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import BottomAppBar from "../components/BottomAppBar";
import "../App.css";

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const recipesResponse = await ApiService.getRecipes();
        setRecipes(recipesResponse.data.lists);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching recipes:", error);
        setError("An error occurred while fetching recipes.");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: "center", paddingTop: "50px" }}>
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div style={{ paddingLeft: "5%", paddingRight: "5%", paddingTop: "5%" }}>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="mt-4">
        <h2>Recipes </h2>
        <ListGroup>
          {recipes.map((recipe) => (
            <ListGroup.Item
              key={recipe.id}
              as={Link}
              to={`/recipe/${recipe.id}`}
              action
            >
              {recipe.name}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </div>

      <div className="position-fixed bottom-0 start-0 w-100">
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Recipes;
