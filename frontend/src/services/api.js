/**
 * API Service
 *
 * Handles all HTTP requests to the backend API.
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication
export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
    username,
    password,
  });
  return response.data;
};

export const register = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/auth/register/`, formData);
  return response.data;
};

export const logout = async () => {
  const token = localStorage.getItem('token');
  if (token) {
    await axios.post(
      `${API_BASE_URL}/auth/logout/`,
      {},
      {
        headers: { Authorization: `Token ${token}` },
      }
    );
  }
};

// Player data
export const getPlayerStats = async (token) => {
  const response = await api.get('/player/stats/', {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const getPlayerInventory = async () => {
  const response = await api.get('/players/inventory/');
  return response.data;
};

// World data
export const getZones = async () => {
  const response = await api.get('/world/zones/');
  return response.data;
};

export const getRooms = async () => {
  const response = await api.get('/rooms/');
  return response.data;
};

// Quests
export const getAvailableQuests = async () => {
  const response = await api.get('/quests/available/');
  return response.data;
};

export default api;
