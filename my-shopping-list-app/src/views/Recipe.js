import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col, Button, Modal, Form } from "react-bootstrap";
import ApiService from "../services/ApiService";
import BottomAppBar from "../components/BottomAppBar";

const List = () => {
  const { recipeId } = useParams();
  const [recipe, setList] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newItemName, setNewItemName] = useState("");
  const [newItemQuantity, setNewItemQuantity] = useState(1);
  const [isAddItemModalOpen, setIsAddItemModalOpen] = useState(false);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const response = await ApiService.getListById(recipeId);
        setList(response.data.list);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching list:", error);
        setError("An error occurred while fetching the list.");
        setLoading(false);
      }
    };

    fetchList();
  }, [recipeId]);

  const handleRecipeToList = async () => {
    try {
      const currentUserResponse = await ApiService.getCurrentUser();
      const currentUser = currentUserResponse.data.user;

      const newListResponse = await ApiService.addList(
        `${recipe.name} Copy`,
        false,
        currentUser.id
      );

      const newListId = newListResponse.data.list_id;

      await Promise.all(
        recipe.items.map(async (item) => {
          await ApiService.addListItem(newListId, item.name, item.quantity, 0);
        })
      );

      const newListResponseUpdated = await ApiService.getListById(newListId);
      setList(newListResponseUpdated.data.list);
    } catch (error) {
      console.error("Error copying list:", error);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: "center", paddingTop: "50px" }}>
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <Container style={{ padding: "20px" }}>
      <h2 className="text-left">{recipe.name}</h2>
      <h3 className="text-left">Ingredients</h3>
      <ul>
        {recipe.items.map((item) => (
          <li key={item.id}>
            <div style={{ display: "flex", alignItems: "center" }}>
              <strong>{item.name} - </strong>
              <div style={{ marginLeft: "5px", marginRight: "5px" }}>
                Needed: {item.quantity}
              </div>
            </div>
          </li>
        ))}
      </ul>
      <Button
        variant="danger"
        className="position-fixed bottom-5 end-5 z-index-1"
        style={{ bottom: "11%", left: "85%" }}
        onClick={() => handleRecipeToList(true)}
      >
        +
      </Button>

      <div className="position-fixed bottom-0 start-0 w-100">
        <BottomAppBar />
      </div>
    </Container>
  );
};

export default List;
