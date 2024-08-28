import { CircularProgress } from '@mui/material';
import React from 'react';
import { AutocompleteInput, Edit, NumberInput, SimpleForm, TextInput } from 'react-admin';
import { getLocations } from '~/api/locations';
import { useNodeChoices } from '~/shared/hooks/use-node-choices';

const LocationsEdit = () => {
  const { choices, isLoading, error } = useNodeChoices('location', () => getLocations());
  if (isLoading) {
    return <CircularProgress />;
  }
  if (error) {
    return <h1>Не удалось загрузить локации</h1>;
  }

  return (
    <Edit>
      <SimpleForm>
        <TextInput source="id" label="id" disabled fullWidth />
        <TextInput source="name" fullWidth />
        <AutocompleteInput choices={choices} source="parent_id" fullWidth disabled />
      </SimpleForm>
    </Edit>
  );
};

export default LocationsEdit;
