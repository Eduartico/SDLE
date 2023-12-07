import React, { useState, useEffect } from "react";
import { Container, Row, Col, Image } from "react-bootstrap";
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
    <div style={{ padding: "20px" }}>
      <Container style={{ padding: "20px" }}>
        <Row>
          <Col>
            <h2>Profile</h2>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {user && (
              <div>
                {user.photo ? (
                  <Image
                    src={user.photo}
                    alt={user.name}
                    roundedCircle
                    className="mb-3"
                  />
                ) : (
                  <Image
                    src="https://via.placeholder.com/100" // Placeholder image URL
                    alt={user.name}
                    roundedCircle
                    className="mb-3"
                  />
                )}
                <h5>{user.name}</h5>
              </div>
            )}
          </Col>
        </Row>

        <Row>
          <Col>
            <div
              className="position-fixed bottom-0 start-0 w-100 bg-light p-2"
              style={{
                position: "fixed",
                bottom: 0,
                left: 0,
                width: "100%",
              }}
            >
              <BottomAppBar />
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Profile;
