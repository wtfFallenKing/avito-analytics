import React, { useMemo } from 'react';
import { useQuery } from 'react-query';
import { Autocomplete, CircularProgress, TextField, Typography } from '@mui/material';
import { useDataProvider } from 'react-admin';
import { Matrix } from '~/entities/matrix';

type MatrixValue = { id: number; label: string };
interface FieldProps {
  value: number | null;
  onChange: (value: number) => any;
}

const BaselineAutoComplete = ({ value, onChange }: FieldProps) => {
  const dataProvider = useDataProvider();
  const { data, isLoading, error } = useQuery(
    ['matrix', 'useGetMany'],
    () => dataProvider.getMany('matrix', {}) as Promise<{ data: Matrix[] }>,
  );
  const matrices = useMemo(
    () => (data ? data.data.filter((matrix) => matrix.type === 'BASE') : []),
    [data],
  );
  const index = useMemo(() => matrices.findIndex((el) => el.id === value), [data, value]);

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error || !data) {
    return <Typography>Не удалось загрузить список матриц</Typography>;
  }

  return (
    <Autocomplete
      value={index === -1 ? null : { id: matrices[index].id, label: matrices[index].name }}
      options={
        (matrices.map((matrix) => ({
          id: matrix.id,
          label: matrix.name,
        })) || []) as MatrixValue[]
      }
      onChange={(_, newValue: MatrixValue | null) => {
        newValue !== null && onChange(newValue.id);
      }}
      renderInput={(params) => <TextField {...params} label="Baseline матрица" />}
      isOptionEqualToValue={(option, v) => option.id === v.id}
    />
  );
};

export default BaselineAutoComplete;
