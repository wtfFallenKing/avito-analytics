import React from 'react';
import { Edit, NumberInput, SimpleForm } from 'react-admin';

function PriceEdit() {
  return (
    <Edit redirect={false}>
      <SimpleForm>
        <NumberInput source="matrix_id" disabled />
        <NumberInput source="location_id" disabled />
        <NumberInput source="category_id" disabled />
        <NumberInput source="price" />
      </SimpleForm>
    </Edit>
  );
}

export default PriceEdit;
