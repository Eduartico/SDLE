import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api'; // TO DO TROCAR URL 
const ApiService = {
  authenticateUser: async (username, password) => {
    const response = await axios.post(`${BASE_URL}/auth/login`, { username, password });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await axios.get(`${BASE_URL}/user/current`); // TO DO TROCAR ENDPOINT
    return response.data;
  },

  getUserLists: async (userId) => {
    console.log(userId);
    const response = await axios.get(`${BASE_URL}/user/${userId}/lists`); // TO DO TROCAR ENDPOINT
    return response.data;
  },

  getListById: async (listId) => {
    const response = await axios.get(`${BASE_URL}/list/${listId}`);
    return response.data;
  }

};

export default ApiService;
