import { api } from './api';
import type { Storage } from '~/entities/storage';

export const getStorage = async (): Promise<Storage | null> => {
  const response = await api.get<Storage>('/storage/configuration');
  if (response.status != 200) {
    return null;
  }
  return response.data;
};

export const setBaseline = async (matrixId: number) => {
  const response = await api.post(`/storage/baseline?baseline=${matrixId}`);
  if (response.status !== 200) {
    throw new Error('Матрица не найдена');
  }
};

export const setDiscounts = async (discounts: number[]) => {
  const response = await api.post('/storage/discounts', {
    discounts,
  });
  if (response.status !== 200) {
    throw new Error('Матрицы не найдены');
  }
};
