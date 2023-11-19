import React, { useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const Home = () => {
  const [user, setUser] = useState(null);
  const [lists, setLists] = useState([]);

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const response = await ApiService.getCurrentUser(); // TODO TROCAR PARA API CALL
        setUser(response.data.user); // Update state com o user
      } catch (error) {
        console.error('Error fetching current user:', error);
      }
    };

    // Fetch listas do user pelo id
    const fetchUserLists = async () => {
      if (user) {
        try {
          const response = await ApiService.getUserLists(user.id); // TODO TROCAR PARA API CALL
          setLists(response.data.lists); 
        } catch (error) {
          console.error('Error fetching user lists:', error);
        }
      }
    };

    fetchCurrentUser();
    fetchUserLists();
  }, []); 


  return (
    <div>
      {/* Botao da sidebar */}
      <div style={{ position: 'fixed', top: '10px', left: '10px', cursor: 'pointer' }}>
        <button onClick={() => console.log('Open Sidebar')}>
          <img
            src="sidebar.png"  {/* Trocar pra icone certo */}
            alt="Sidebar Icon"
            style={{ width: '30px', height: '30px' }} 
          />
        </button>
      </div>

      <div>
        {/* Lista das listas do user */}
        <h2>Your Shopping Lists</h2>
        <ul>
          {lists.map((list) => (
            <li key={list.id}>{list.name}</li>
          ))}
        </ul>
      </div>

      {/* Barra de baixo */}
      <div style={{ position: 'fixed', bottom: 0, left: 0, width: '100%', background: '#f0f0f0', padding: '10px' }}>
        TO DO BARRA.
      </div>
    </div>
  );
};

export default Home;