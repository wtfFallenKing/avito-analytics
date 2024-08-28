import React from 'react';
import {
  Admin,
  CustomRoutes,
  Resource,
  ShowGuesser,
  localStorageStore,
  useStore,
  StoreContextProvider,
} from 'react-admin';

import { dataProvider } from '~/providers';
import { i18nProvider } from './i18n';

import CustomLayout from '~/layout/layout';

import { LocationsEdit, LocationsList, LocationsShow } from '~/resources/locations';
import { CategoriesEdit, CategoriesList, CategoriesShow } from '~/resources/categories';
import { MatricesList, MatrixCreate } from '~/resources/matrices';
import MatrixEdit from '~/resources/matrices/edit';
import { themes, ThemeName } from '~/themes/themes';
import './global.css';
import Dashboard from '~/resources/Dashboard';
import PriceEdit from '~/resources/prices/edit';
import StorageLogsList from '~/resources/storage-logs/list';
import MatrixLogsList from '~/matrix_logs/list';

const store = localStorageStore(undefined, 'avito-analytics');

function App() {
  const [themeName] = useStore<ThemeName>('themeName', 'house');
  const lightTheme = themes.find((theme) => theme.name === themeName)?.light;
  const darkTheme = themes.find((theme) => theme.name === themeName)?.dark;
  return (
    <Admin
      title=""
      dataProvider={dataProvider}
      layout={CustomLayout}
      i18nProvider={i18nProvider}
      darkTheme={darkTheme}
      lightTheme={lightTheme}
      store={store}
      dashboard={Dashboard}
      disableTelemetry
      defaultTheme="light"
    >
      <Resource
        name="matrix"
        list={MatricesList}
        edit={MatrixEdit}
        show={ShowGuesser}
        create={MatrixCreate}
      />
      <Resource name="location" list={LocationsList} edit={LocationsEdit} show={LocationsShow} />
      <Resource name="category" list={CategoriesList} edit={CategoriesEdit} show={CategoriesShow} />
      <Resource name="price" edit={PriceEdit} />
      <Resource name="storage_logs" list={StorageLogsList} />
      <Resource name="matrix_logs" list={MatrixLogsList} />
    </Admin>
  );
}

const AppWrapper = () => (
  <StoreContextProvider value={store}>
    <App />
  </StoreContextProvider>
);

export default AppWrapper;
