import type { DataProvider, GetListResult } from 'react-admin';
import { Price } from '~/entities';
import { api } from '~/api/api';

type PriceResponse = Omit<Price, 'id'>;

const getId = ({
  category_id,
  location_id,
  matrix_id,
}: Pick<Price, 'category_id' | 'location_id' | 'matrix_id'>) =>
  `${location_id}-${category_id}-${matrix_id}`;

const handlePriceResponse = (response: PriceResponse[]) =>
  response.map(
    ({ category_id, location_id, matrix_id, price }: PriceResponse): Price => ({
      location_id,
      category_id,
      matrix_id,
      price,
      id: getId({ category_id, location_id, matrix_id }),
    }),
  );

export const priceProvider: DataProvider = {
  getList: async (resource, params): Promise<GetListResult<Price>> => {
    const response = await api.get<PriceResponse[]>('/price');
    return {
      data: handlePriceResponse(response.data),
      total: response.headers['x-total-count'],
    };
  },
  getManyReference: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const response = await api.get<PriceResponse[]>(
      `/price/${params.id}?_end=${perPage * page}&_start=${perPage * (page - 1)}`,
    );
    return {
      data: handlePriceResponse(response.data),
      total: response.headers['x-total-count'],
    };
  },
  getOne: async (resource, params) => {
    const [category_id, location_id, matrix_id] = `${params.id}`
      .split('-')
      .map((el) => parseInt(el, 10));
    const response = await api.get<PriceResponse>(
      `/price/${location_id}/${category_id}/${matrix_id}`,
    );

    return {
      data: { ...response.data, id: params.id },
    };
  },
  update: async (resource, params) => {
    const { price, id } = params.data;
    const [location_id, category_id, matrix_id] = `${id}`.split('-').map((el) => parseInt(el, 10));
    console.log({
      category_id,
      location_id,
      matrix_id,
      price,
    });
    await api.put('/price', {
      category_id,
      location_id,
      matrix_id,
      price,
    });
    return {
      data: (await priceProvider.getOne(resource, params)).data,
    };
  },
};
