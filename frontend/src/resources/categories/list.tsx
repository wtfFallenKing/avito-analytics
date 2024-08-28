import React from 'react';
import { List, Datagrid, TextField, TopToolbar, ExportButton, SelectField } from 'react-admin';
import { getCategories, uploadCategotyCsv } from '~/api/categories';
import { useNodeChoices } from '~/shared/hooks/use-node-choices';
import UploadButton from '~/shared/upload-button';

const ListActions = () => {
  return (
    <TopToolbar>
      <UploadButton onUpload={uploadCategotyCsv} />
      <ExportButton />
    </TopToolbar>
  );
};

export const CategoriesList = () => {
  const { choices } = useNodeChoices('location', () => getCategories());
  return (
    <List actions={<ListActions />} empty={false}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" />
        <SelectField source="parent_id" choices={choices} />
      </Datagrid>
    </List>
  );
};

export default CategoriesList;
