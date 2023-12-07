import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ApiService from "../services/ApiService";
import { Button, ListGroup, Modal } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import BottomAppBar from "../components/BottomAppBar";

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

  const handleAddList = (e) => {
    e.preventDefault();

    const newList = {
      id: Math.random().toString(),
      name: newListName,
      usernames: newListUsernames.split(",").map((username) => username.trim()),
    };

    setLists((prevLists) => [...prevLists, newList]);

    setIsAddListModalOpen(false);
    setNewListName("");
    setNewListUsernames("");
  };

  return (
    <div>
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
        className="position-fixed bottom-3 end-3"
        onClick={() => setIsAddListModalOpen(true)}
      >
        +
      </Button>

      {/* Add List Modal */}
      <Modal show={isAddListModalOpen} onHide={() => setIsAddListModalOpen(false)}>
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
          </form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" type="submit">
              Add List
          </Button>
          <Button variant="secondary" onClick={() => setIsAddListModalOpen(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <div className="position-fixed bottom-0 start-0 w-100 bg-light p-2">
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Home;
