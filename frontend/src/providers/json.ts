import jsonServerProvider from 'ra-data-json-server';

import { api } from '~/api/api';

const provider = jsonServerProvider(import.meta.env.VITE_API_BASE);

export const jsonProvider = {
  ...provider,
  create: async (resource, params) => {
    if (resource !== 'matrix') {
      return provider.create(resource, params);
    }
    const { data } = params;
    const form = new FormData();
    form.append('file', data.file.rawFile);
    return await api.post(
      `/matrix?name=${data.name}${data.segment_id === undefined ? '' : '&segment_id=' + data.segment_id}`,
      form,
    );
  },
};
