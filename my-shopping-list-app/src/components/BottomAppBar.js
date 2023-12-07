import React from "react";
import { Link } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import { Home, Restaurant, AccountCircle } from "@mui/icons-material";

const BottomAppBar = () => {
  return (
    <div>
      <Container fluid style={{ background: "gray", padding: "10px" }}>
        <Row className="justify-content-center align-items-center">
          <Col className="text-center">
            <Link to="/home">
              <Home fontSize="large" style={{ color: "white" }} />
            </Link>
          </Col>
          <Col className="text-center">
            <Link to="/recipes">
              <Restaurant fontSize="large" style={{ color: "white" }} />
            </Link>
          </Col>
          <Col className="text-center">
            <Link to="/profile">
              <AccountCircle fontSize="large" style={{ color: "white" }} />
            </Link>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default BottomAppBar;
