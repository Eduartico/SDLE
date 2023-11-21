import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; 
import ApiService from '../services/ApiService';

const Home = () => {
  const [user, setUser] = useState(null);
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch current user
        const userResponse = await ApiService.getCurrentUser();
        setUser(userResponse.data.user);

        // Fetch user's lists
        const listsResponse = await ApiService.getUserLists(userResponse.data.user.id);
        setLists(listsResponse.data.lists);

        setLoading(false); 
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('An error occurred while fetching data.');
        setLoading(false); 
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <div style={{ position: 'fixed', top: '10px', left: '10px', cursor: 'pointer' }}>
        <button onClick={() => console.log('Open Sidebar')}>
          <img
            src="sidebar.png"  //TO DO TROCAR ICONE
            alt="Sidebar Icon"
            style={{ width: '30px', height: '30px' }}
          />
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {error && <p style={{ color: 'red' }}>{error}</p>}

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

      <div style={{ position: 'fixed', bottom: 0, left: 0, width: '100%', background: '#f0f0f0', padding: '10px' }}>
        TO DO BOTTOM BAR.
      </div>
    </div>
  );
};

export default Home;
