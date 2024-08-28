import React from 'react';
import { Create, SimpleForm, TextInput, FileInput } from 'react-admin';

function MatrixCreate() {
  return (
    <Create>
      <SimpleForm>
        <TextInput source="name" required />
        <TextInput source="segment_id" helperText="Для Baseline матрицы оставить пустым" />
        <FileInput source="file" isRequired />
      </SimpleForm>
    </Create>
  );
}

export default MatrixCreate;
