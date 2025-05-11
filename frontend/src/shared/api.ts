import axios from 'axios';
import type { AnimalDetails } from '../components/AnimalCard'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

export const getAnimals = () =>
  api.get('/animals').then(res => res.data);

/** детали одного животного по id */
export const getAnimal = (id: number) => api
  .get<AnimalDetails>(`/animals/${id}`)
  .then(r => r.data);