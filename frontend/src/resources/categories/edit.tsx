import { CircularProgress } from '@mui/material';
import React from 'react';
import { AutocompleteInput, Edit, SimpleForm, TextInput } from 'react-admin';
import { getCategories } from '~/api/categories';
import { useNodeChoices } from '~/shared/hooks/use-node-choices';

const CategoriesEdit = () => {
  const { choices, isLoading, error } = useNodeChoices('category', () => getCategories());

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error) {
    return <h1>Не удалось загрузить категории</h1>;
  }

  return (
    <Edit>
      <SimpleForm>
        <TextInput source="id" label="id" fullWidth disabled />
        <TextInput source="name" fullWidth />
        <AutocompleteInput source="parent_id" choices={choices} fullWidth disabled />
      </SimpleForm>
    </Edit>
  );
};

export default CategoriesEdit;
