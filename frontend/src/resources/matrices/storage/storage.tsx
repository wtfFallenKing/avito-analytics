import React, { useEffect, useMemo, useState } from 'react';
import { useQuery } from 'react-query';
import { Box, Button, Card, CardContent, CircularProgress, Typography } from '@mui/material';
import { getStorage, setBaseline, setDiscounts } from '~/api/storage';

import BaselineAutoComplete from './baseline';
import DiscountsSwitches from './discounts';
import { useRefresh } from 'react-admin';

type Form = { baseline: number | null; discounts: number[] };

function Storage() {
  const { data, isLoading, error } = useQuery('storage', () => getStorage());
  const refresh = useRefresh();

  const [form, setForm] = useState<Form>({
    baseline: null,
    discounts: [],
  });

  const isChanged = useMemo(() => {
    if (!data) {
      return false;
    }
    return !(
      data.baseline === form.baseline &&
      data.discounts.every((value, index) => form.discounts[index] === value) &&
      data.discounts.length === form.discounts.length
    );
  }, [data, form]);

  useEffect(() => {
    if (data && data !== null && !isLoading && !error) {
      setForm({
        ...form,
        baseline: data.baseline,
        discounts: data.discounts,
      });
    }
  }, [data, isLoading, error]);

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error) {
    return <h1>Не удалось загрузить список матриц</h1>;
  }

  const updateStorage = async () => {
    if (form.baseline !== null) {
      await setBaseline(form.baseline);
    }
    await setDiscounts(form.discounts);
    refresh();
  };

  return (
    <Card
      sx={{
        m: 1,
      }}
    >
      <CardContent
        sx={{
          width: 300,
        }}
      >
        <Typography align="center">Активные матрицы</Typography>
        <BaselineAutoComplete
          value={form.baseline}
          onChange={(value) =>
            setForm((newForm) => ({
              ...newForm,
              baseline: value,
            }))
          }
        />
        <Typography align="center">Скидочные матрицы</Typography>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Typography>Название</Typography>
          <Typography>Используется?</Typography>
        </Box>
        <DiscountsSwitches
          value={form.discounts}
          onChange={(value) =>
            setForm((newForm) => ({
              ...newForm,
              discounts: value,
            }))
          }
        />
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <Button variant="contained" color="primary" disabled={!isChanged} onClick={updateStorage}>
            Сохранить
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}

export default Storage;
