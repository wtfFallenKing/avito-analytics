import { combineDataProviders } from 'react-admin';

import { jsonProvider } from './json';
import { priceProvider } from './prices';

export const dataProvider = combineDataProviders((resource) => {
  switch (resource) {
    case 'price':
      return priceProvider;
    default:
      return jsonProvider;
  }
});
