import { api } from './api';
import type { Node } from '~/entities';

export const getLocations = async () => {
  const response = await api.get<Node[]>('/location?_start=0&_end=10000');
  if (response.status !== 200) {
    throw new Error('Невозможно получить локации');
  }
  return response.data;
};

export const uploadLocationCsv = async (file: File) => {
  const form = new FormData();
  form.append('file', file);
  const response = await api.post('/location/csv', form);
  return response.status >= 200 && response.status < 400;
};
