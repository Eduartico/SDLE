import React from "react";
import { Link } from "react-router-dom";
import HomeIcon from "@mui/icons-material/Home";
import RestaurantIcon from "@mui/icons-material/Restaurant";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

const BottomAppBar = () => {
  return (
    <div
      className="bottom-app-bar"
      style={{ display: "flex", justifyContent: "space-around" }}
    >
      <Link to="/home">
        <HomeIcon fontSize="large" />
      </Link>
      <Link to="/recipes">
        <RestaurantIcon fontSize="large" />
      </Link>
      <Link to="/profile">
        <AccountCircleIcon fontSize="large" />
      </Link>
    </div>
  );
};

export default BottomAppBar;
