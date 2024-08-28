import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  TopToolbar,
  CreateButton,
  ExportButton,
  SelectField,
} from 'react-admin';
import Storage from './storage/storage';

const ListActions = () => {
  return (
    <TopToolbar>
      <CreateButton label="Загрузить CSV" />
      <ExportButton />
    </TopToolbar>
  );
};

export const MatricesList = () => (
  <List empty={false} aside={<Storage />} actions={<ListActions />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <SelectField
        source="type"
        choices={[
          { id: 'BASE', name: 'Основная' },
          { id: 'DISCOUNT', name: 'Скидочная' },
        ]}
      />
      <TextField source="segment_id" />
    </Datagrid>
  </List>
);

export default MatricesList;
