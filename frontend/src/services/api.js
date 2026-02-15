import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchCostData = async () => {
  const response = await api.get('/api/costs');
  return response.data;
};
