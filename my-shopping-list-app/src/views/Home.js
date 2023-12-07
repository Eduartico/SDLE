import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ApiService from "../services/ApiService";
import sidebarIcon from "../icons/sidebar.png";
import BottomAppBar from "../components/BottomAppBar";

const Home = () => {
  const [user, setUser] = useState(null);
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newListName, setNewListName] = useState('');
  const [newListUsernames, setNewListUsernames] = useState('');
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
      id: Math.random().toString(),  // THIS SHOULD BE DONE BY BACKEND 
      name: newListName,
      usernames: newListUsernames.split(',').map(username => username.trim()),
    };

    setLists((prevLists) => [...prevLists, newList]);

    setIsAddListModalOpen(false);
    setNewListName('');
    setNewListUsernames('');
  };

  return (
    <div>

      {loading && <p>Loading...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div>
        <h2>Your Shopping Lists</h2>
        <ul>
          {lists.map((list) => (
            <li key={list.id}>
              <Link to={`/list/${list.id}`}>{list.name}</Link>
            </li>
          ))}
        </ul>
      </div>
      <button
        style={{ position: 'fixed', bottom: '70px', right: '10px', cursor: 'pointer' }}
        onClick={() => setIsAddListModalOpen(true)}
      >
        +
      </button>

      {/* Add List Modal */}
      {isAddListModalOpen && (
        <div
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            background: 'white',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
            zIndex: 9999,
          }}
        >
          <h3>Add New List</h3>
          <form onSubmit={handleAddList}>
            <label>
              List Name:
              <input
                type="text"
                value={newListName}
                onChange={(e) => setNewListName(e.target.value)}
                required
              />
            </label>
            <label>
              Usernames (comma-separated):
              <input
                type="text"
                value={newListUsernames}
                onChange={(e) => setNewListUsernames(e.target.value)}
                required
              />
            </label>
            <button type="button" onClick={handleAddList}>
              Add List
            </button>
          </form>
          <button onClick={() => setIsAddListModalOpen(false)}>Close</button>
        </div>
      )}

      <div
        style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          width: "100%",
          background: "#f0f0f0",
          padding: "10px",
        }}
      >
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Home;
