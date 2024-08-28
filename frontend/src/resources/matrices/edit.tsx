import { Box, CircularProgress } from '@mui/material';
import React from 'react';
import {
  Datagrid,
  Edit,
  Form,
  List,
  NumberField,
  NumberInput,
  Pagination,
  ReferenceManyField,
  SaveButton,
  SelectField,
  SelectInput,
  SimpleForm,
  TextInput,
} from 'react-admin';
import { getCategories } from '~/api/categories';
import { getLocations } from '~/api/locations';
import { useNodeChoices } from '~/shared/hooks/use-node-choices';

const MatrixEdit = () => {
  const {
    choices: categories,
    isLoading: isCategoriesLoading,
    error: categoriesError,
  } = useNodeChoices('category', () => getCategories());
  const {
    choices: locations,
    isLoading: isLocationsLoading,
    error: locationsError,
  } = useNodeChoices('location', () => getLocations());

  if (isCategoriesLoading || isLocationsLoading) {
    return <CircularProgress />;
  }

  if (categoriesError || locationsError) {
    return <h1>Не удалось загрузить категории</h1>;
  }

  return (
    <Edit>
      <Form>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 5 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <NumberInput source="id" disabled />
            <TextInput source="name" />
            <SelectInput
              source="type"
              choices={[
                { id: 'BASE', name: 'Основная' },
                { id: 'DISCOUNT', name: 'Скидочная' },
              ]}
              isRequired
              disabled
            />
            <NumberInput source="segment_id" />
            <SaveButton />
          </Box>
          <Box
            sx={{
              width: '80%',
            }}
          >
            <ReferenceManyField reference="price" target="matrix_id" pagination={<Pagination />}>
              <Datagrid rowClick="edit">
                <NumberField source="matrix_id" />
                <SelectField source="category_id" choices={categories} />
                <SelectField source="location_id" choices={locations} />
                <NumberField source="price" />
              </Datagrid>
            </ReferenceManyField>
          </Box>
        </Box>
      </Form>
    </Edit>
  );
};

export default MatrixEdit;
