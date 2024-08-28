import React from 'react';
import { List, Datagrid, TextField } from 'react-admin';

export const PricesList = () => {
  return (
    <List>
      <Datagrid rowClick="show">
        <TextField source="location_id" />
        <TextField source="category_id" />
        <TextField source="price" />
      </Datagrid>
    </List>
  );
};

export default PricesList;
