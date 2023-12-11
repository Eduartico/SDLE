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
  const [isFlipped, setIsFlipped] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setIsFlipped((prevIsFlipped) => !prevIsFlipped);
    }, 3000);

    return () => clearInterval(intervalId);
  }, []);

  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  useEffect(() => {
    const fetchData = async () => {
      await delay(500);
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
  }, [isFlipped, isAddListModalOpen]);

  const handleAddList = async (e) => {
    e.preventDefault();
    try {
      const newListResponse = await ApiService.addList(
        newListName,
        false,
        newListUsernames + "," + user.id
      );

      const newList = {
        id: newListResponse.data.list_id,
        name: newListName,
        usersId: newListUsernames
          .split(",")
          .map((username) => username.trim())
          .filter((username) => username !== "," && !isNaN(username)),
      };

      setLists((prevLists) => [...prevLists, newList]);
    } catch (error) {
      console.error("Error adding new list:", error);
    }

    setIsAddListModalOpen(false);
    setNewListName("");
    setNewListUsernames("");
  };

  const handleToggleOnlineStatus = async () => {
    if (!user || !user.id) {
      console.error('User ID is null or invalid.');
      return;
    }

    try {
      const updatedStatus = !user.online; // Toggle the online status
      await ApiService.setOnlineStatus(updatedStatus);

      // Atualize o estado local do usuário
      setUser((prevUser) => ({ ...prevUser, online: updatedStatus }));
    } catch (error) {
      console.error('Error updating online status:', error);
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

      <Button
        variant="outline-danger"
        className="position-fixed top-5 end-5 z-index-1"
        style={{ top: "2%", left: "85%" }}
        onClick={handleToggleOnlineStatus}
      >
        {user.online ? "Go Offline" : "Go Online"}
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
