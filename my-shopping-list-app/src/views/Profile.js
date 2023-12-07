import React, { useState, useEffect } from "react";
import { Avatar, Typography } from "@mui/material";
import ApiService from "../services/ApiService";
import BottomAppBar from "../components/BottomAppBar";

const Profile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await ApiService.getCurrentUser();
        setUser(response.data.user);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError("An error occurred while fetching user data.");
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  return (
    <div>
      <div>
        <h2>Profile</h2>

        {loading && <p>Loading...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {user && (
          <div>
            {user.photo ? (
              <Avatar
                alt={user.name}
                src={user.photo}
                sx={{ width: 100, height: 100 }}
              />
            ) : (
              <Avatar sx={{ width: 100, height: 100 }}>{user.name && user.name[0]}</Avatar>
            )}
            <Typography variant="h5">{user.name}</Typography>
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
    </div>
  );
};

export default Profile;
