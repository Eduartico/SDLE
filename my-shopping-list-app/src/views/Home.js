import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ApiService from "../services/ApiService";
import { Button, ListGroup, Modal } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import BottomAppBar from "../components/BottomAppBar";
import "../App.css";

const Home = () => {
  const [user, setUser] = useState(null);
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newListName, setNewListName] = useState("");
  const [newListUsernames, setNewListUsernames] = useState("");
  const [isAddListModalOpen, setIsAddListModalOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userResponse = await ApiService.getCurrentUser();
        setUser(userResponse.data.user);

        const listsResponse = await ApiService.getUserLists(
          userResponse.data.user.id
        );
        setLists(listsResponse.data.lists);

        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("An error occurred while fetching data.");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddList = async (e) => {
    e.preventDefault();
  
    try {
      const newListResponse = await ApiService.addList(newListName, false, user.id);
  
      const newList = {
        id: newListResponse.data.list_id,
        name: newListName,
        usernames: newListUsernames.split(",").map((username) => username.trim()),
      };
  
      setLists((prevLists) => [...prevLists, newList]);
    } catch (error) {
      console.error('Error adding new list:', error);
    }
  
    setIsAddListModalOpen(false);
    setNewListName("");
    setNewListUsernames("");
  };

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
      {loading && <p>Loading...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="mt-4">
        <h2>Your Shopping Lists</h2>
        <ListGroup>
          {lists.map((list) => (
            <ListGroup.Item
              key={list.id}
              as={Link}
              to={`/list/${list.id}`}
              action
            >
              {list.name}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </div>

      <Button
        variant="danger"
        className="position-fixed bottom-5 end-5 z-index-1"
        style={{ bottom: "11%", left: "85%" }}
        onClick={() => setIsAddListModalOpen(true)}
      >
        +
      </Button>

      <Modal
        show={isAddListModalOpen}
        onHide={() => setIsAddListModalOpen(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title>Add New List</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form onSubmit={handleAddList}>
            <label>
              List Name:
              <input
                type="text"
                className="form-control"
                value={newListName}
                onChange={(e) => setNewListName(e.target.value)}
                required
              />
            </label>
            <label>
              Usernames (comma-separated):
              <input
                type="text"
                className="form-control"
                value={newListUsernames}
                onChange={(e) => setNewListUsernames(e.target.value)}
                required
              />
            </label>
            <div>
              <Button variant="danger" type="submit" className="mt-3">
                Add List
              </Button>
            </div>
          </form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setIsAddListModalOpen(false)}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      <div className="position-fixed bottom-0 start-0 w-100">
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Home;
