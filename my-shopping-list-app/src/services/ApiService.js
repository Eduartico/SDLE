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
  },

  updateListById: async (request) => {
    // Request example:
    // {"name": "My List", "listId": "1", "isRecipe": false}
    const response = await axios.put(`${BASE_URL}/updateList`, request);
    return response.data;
  },

  updateListItemById: async (request) => {
    // Request example:
    // {"name": "My Item", "itemId": "1", "quantity": 3, "boughtQuantity": 2}
    const response = await axios.put(`${BASE_URL}/updateListItem`, request);
    return response.data;
  },

  createList: async (list) => {
    // Request example:
    // {"name": "My List", "userId": "1", "isRecipe": false}
    const response = await axios.post(`${BASE_URL}/addList`, list);
    return response.data;
  },

  createListItem: async (request) => {
    // Request example:
    // {"name": "My Item", "listId": "1", "quantity": 3, "boughtQuantity": 2}
    const response = await axios.post(`${BASE_URL}/addListItem`, request);
    return response.data;
  },
  
  deleteListById: async (request) => {
    // Request example:
    // {"listId": "1"}
    const response = await axios.delete(`${BASE_URL}/deleteList`, request);
    return response.data;
  },

  deleteListItemById: async (request) => {
    // Request example:
    // {"itemId": "1"}
    const response = await axios.delete(`${BASE_URL}/deleteListItem`, request);
    return response.data;
  },

};

export default ApiService;
