import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col, Button, Modal, Form } from "react-bootstrap";
import ApiService from "../services/ApiService";
import BottomAppBar from "../components/BottomAppBar";

const List = () => {
  const { listId } = useParams();
  const [list, setList] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newItemName, setNewItemName] = useState("");
  const [newItemQuantity, setNewItemQuantity] = useState(1);
  const [isAddItemModalOpen, setIsAddItemModalOpen] = useState(false);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const response = await ApiService.getListById(listId);
        setList(response.data.list);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching list:", error);
        setError("An error occurred while fetching the list.");
        setLoading(false);
      }
    };

    fetchList();
  }, [listId]);

  const handleQuantityChange = async (itemId, newQuantity) => {
    try {
      // Atualiza localmente o estado da lista
      setList((prevList) => {
        const updatedItems = prevList.items.map((item) => {
          if (item.id === itemId) {
            const boughtQuantity = Math.max(0, Math.min(newQuantity, item.quantity));
  
            // Chamada à API para atualizar boughtQuantity na base de dados
            ApiService.updateItemBoughtQuantity(listId, itemId, boughtQuantity);
  
            return { ...item, boughtQuantity };
          }
          return item;
        });
  
        return { ...prevList, items: updatedItems };
      });
    } catch (error) {
      console.error("Error updating item quantity:", error);
    }
  };

  const handleToggleDone = async (itemId) => {
    try {
      const currentItem = list.items.find((item) => item.id === itemId);
      const newBoughtQuantity = currentItem.boughtQuantity === 0 ? currentItem.quantity : 0;
  
      // Atualiza o estado local
      setList((prevList) => {
        const updatedItems = prevList.items.map((item) =>
          item.id === itemId ? { ...item, boughtQuantity: newBoughtQuantity } : item
        );
        return { ...prevList, items: updatedItems };
      });
  
      // Atualiza a base de dados apenas se necessário
      if (currentItem.boughtQuantity !== newBoughtQuantity) {
        await ApiService.buyListItem(listId, itemId, { boughtQuantity: newBoughtQuantity });
      }
    } catch (error) {
      console.error("Error updating item status:", error);
    }
  };

  const handleAddItem = async (e) => {
    e.preventDefault();
  
    try {
      const newItemResponse = await ApiService.addListItem(
        list.id,
        newItemName,
        newItemQuantity,
        0 
      );
  
      const newItem = {
        id: newItemResponse.data.item_id,
        name: newItemName,
        quantity: newItemQuantity,
        boughtQuantity: 0,
      };
  
      setList((prevList) => ({
        ...prevList,
        items: [...prevList.items, newItem],
      }));
    } catch (error) {
      console.error("Error adding new item:", error);
    }
  
    setNewItemName("");
    setNewItemQuantity(1);
    setIsAddItemModalOpen(false);
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
      <h2 className="text-left">{list.name}</h2>
      {/* Needed items */}
      <h3 className="text-left">Needed</h3>
      <ul>
        {list.items
          .filter((item) => item.boughtQuantity < item.quantity)
          .map((item) => (
            <li key={item.id}>
              <div style={{ display: "flex", alignItems: "center" }}>
                <strong>{item.name} - </strong>
                <div style={{ marginLeft: "5px", marginRight: "5px" }}>
                  Needed: {item.quantity}
                </div>
                <Form.Check
                  type="checkbox"
                  label="Bought"
                  checked={item.boughtQuantity === item.quantity}
                  onChange={() => handleToggleDone(item.id)}
                />
                {item.quantity > 1 && (
                  <div style={{ marginLeft: "5px" }}>
                    {item.quantity > 1 && (
                      <>
                        {item.boughtQuantity > 0 && (
                          <Button
                            variant="danger"
                            size="sm"
                            onClick={() => handleQuantityChange(item.id, item.boughtQuantity - 1)}
                          >
                            -
                          </Button>
                        )}
                        <span style={{ margin: "0 5px" }}>{item.boughtQuantity}</span>
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => handleQuantityChange(item.id, item.boughtQuantity + 1)}
                        >
                          +
                        </Button>
                      </>
                    )}
                  </div>
                )}
              </div>
            </li>
          ))}
      </ul>

      {/* Done items */}
      <h3 className="text-left">Done</h3>
      <ul>
        {list.items
          .filter((item) => item.boughtQuantity === item.quantity)
          .map((item) => (
            <li key={item.id}>
              <div style={{ display: "flex", alignItems: "center" }}>
                <strong>{item.name} - </strong>
                <div style={{ marginLeft: "5px", marginRight: "5px" }}>
                  Needed: {item.quantity}
                </div>
                <Form.Check
                  type="checkbox"
                  label="Bought"
                  checked={item.boughtQuantity === item.quantity}
                  onChange={() => handleToggleDone(item.id)}
                />
                {item.quantity > 1 && (
                  <div style={{ marginLeft: "5px" }}>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() =>
                        handleQuantityChange(
                          item.id,
                          Math.max(1, item.boughtQuantity - 1)
                        )
                      }
                    >
                      -
                    </Button>
                    <span style={{ margin: "0 5px" }}>
                      {item.boughtQuantity}
                    </span>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() =>
                        handleQuantityChange(item.id, item.boughtQuantity + 1)
                      }
                    >
                      +
                    </Button>
                  </div>
                )}
              </div>
            </li>
          ))}
      </ul>
      <Button
        variant="danger"
        className="position-fixed bottom-5 end-5 z-index-1"
        style={{ bottom: "11%", left: "85%" }}
        onClick={() => setIsAddItemModalOpen(true)}
      >
        +
      </Button>

      {/* Add Item Modal */}
      <Modal
        show={isAddItemModalOpen}
        onHide={() => setIsAddItemModalOpen(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title>Add New Item</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleAddItem}>
            <Form.Group controlId="formItemName">
              <Form.Label>Name:</Form.Label>
              <Form.Control
                type="text"
                value={newItemName}
                onChange={(e) => setNewItemName(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formItemQuantity">
              <Form.Label>Quantity:</Form.Label>
              <Form.Control
                type="number"
                value={newItemQuantity}
                onChange={(e) =>
                  setNewItemQuantity(parseInt(e.target.value, 10))
                }
                min="1"
                required
              />
            </Form.Group>

            <Button variant="danger" type="submit" className="mt-3">
              Add Item
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setIsAddItemModalOpen(false)}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <div className="position-fixed bottom-0 start-0 w-100">
        <BottomAppBar />
      </div>
    </Container>
  );
};

export default List;
