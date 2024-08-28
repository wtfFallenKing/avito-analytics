import React, { useMemo } from 'react';
import { useQuery } from 'react-query';
import { Box, CircularProgress, Switch, Typography } from '@mui/material';
import { useDataProvider } from 'react-admin';
import { Matrix } from '~/entities/matrix';

interface DiscountsSwitchesProps {
  value: number[];
  onChange: (value: number[]) => any;
}

const DiscountsSwitches = ({ value, onChange }: DiscountsSwitchesProps) => {
  const dataProvider = useDataProvider();
  const { data, isLoading, error } = useQuery(
    ['matrix', 'useGetMany'],
    () =>
      dataProvider.getMany('matrix', {
        ids: [],
      }) as Promise<{ data: Matrix[] }>,
  );
  const matirces = useMemo(
    () => (data ? data.data.filter((matrix) => matrix.type === 'DISCOUNT') : []),
    [data],
  );

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error || !data) {
    return <Typography>Не удалось загрузить список матриц</Typography>;
  }

  return (
    <Box>
      {matirces.map((matrix) => (
        <Box
          key={matrix.id}
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Typography>{matrix.name}</Typography>
          <Switch
            checked={value.includes(matrix.id)}
            onChange={() => {
              if (value.includes(matrix.id)) {
                onChange(value.filter((id) => id !== matrix.id));
              } else {
                onChange([...value, matrix.id]);
              }
            }}
          />
        </Box>
      ))}
    </Box>
  );
};

export default DiscountsSwitches;
