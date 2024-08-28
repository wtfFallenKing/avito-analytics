import { CircularProgress } from '@mui/material';
import React, { useMemo } from 'react';
import {
  List,
  Datagrid,
  TextField,
  TopToolbar,
  ExportButton,
  AutocompleteInput,
  ReferenceInput,
  SelectField,
} from 'react-admin';
import { useQuery } from 'react-query';

import { getLocations, uploadLocationCsv } from '~/api/locations';
import { useNodeChoices } from '~/shared/hooks/use-node-choices';
import UploadButton from '~/shared/upload-button';

const ListActions = () => {
  return (
    <TopToolbar>
      <UploadButton onUpload={uploadLocationCsv} />
      <ExportButton />
    </TopToolbar>
  );
};

export const LocationsList = () => {
  const { choices } = useNodeChoices('location', () => getLocations());
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

export default LocationsList;
