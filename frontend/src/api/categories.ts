import { api } from './api';
import type { Node } from '~/entities';

export const getCategories = async () => {
  const response = await api.get<Node[]>('/category');
  if (response.status !== 200) {
    throw new Error('Невозможно получить категории');
  }
  return response.data;
};

export const uploadCategotyCsv = async (file: File) => {
  const form = new FormData();
  form.append('file', file);
  const response = await api.post('/category/csv', form);
  return response.status >= 200 && response.status < 400;
};
