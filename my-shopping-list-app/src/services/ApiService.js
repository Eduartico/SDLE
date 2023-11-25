import axios from 'axios';

const BASE_URL = 'http://your-api-base-url.com'; // TO DO TROCAR URL 
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
    const response = await axios.get(`${BASE_URL}/user/${userId}/lists`); // TO DO TROCAR ENDPOINT
    return response.data;
  },

};

export default ApiService;
