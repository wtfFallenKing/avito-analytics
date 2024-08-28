import { Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';
import { BarChart, LineChart, PieChart } from '@mui/x-charts';
import React from 'react';
import { Title } from 'react-admin';
import { useQuery } from 'react-query';
import { api } from '~/api/api';
import { green, purple } from '@mui/material/colors';

const getAnalyticsInfo = async () => {
  return await api.get('storage/analytics');
};

const Dashboard = () => {
  const { data, isLoading, isError } = useQuery('dataStorage', () => getAnalyticsInfo());
  const obj = data?.data;

  console.log(obj);

  return (
    <Card>
      <Title title="Главная страница" />
      <CardContent>
        {isLoading ? (
          <CircularProgress />
        ) : isError ? (
          <Typography>Ошибка при загрузке данных для графиков</Typography>
        ) : (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between' }}>
            <Box>
              <BarChart
                xAxis={[
                  {
                    scaleType: 'band',
                    data: Object.keys(obj?.categories),
                    tickLabelStyle: {
                      angle: 90,
                      textAnchor: 'start',
                      fontSize: 15,
                      fontWeight: 600,
                    },
                  },
                ]}
                yAxis={[
                  {
                    data: Object.values(obj?.categories),
                    tickLabelStyle: { textAnchor: 'end', fontSize: 15, fontWeight: 600 },
                  },
                ]}
                series={[{ data: Object.values(obj?.categories), color: '#DE196B' }]}
                width={600}
                height={400}
              />
              <Typography align="center">Популярность по категориям</Typography>
            </Box>
            <Box>
              <BarChart
                xAxis={[
                  {
                    scaleType: 'band',
                    data: Object.keys(obj?.locations),
                    tickLabelStyle: {
                      angle: 90,
                      textAnchor: 'start',
                      fontSize: 15,
                      fontWeight: 600,
                    },
                  },
                ]}
                yAxis={[
                  {
                    data: Object.values(obj?.locations),
                    tickLabelStyle: { textAnchor: 'end', fontSize: 15, fontWeight: 600 },
                  },
                ]}
                series={[{ data: Object.values(obj?.locations), color: '#DE196B' }]}
                width={600}
                height={400}
              />
              <Typography align="center">Популярность по локациям</Typography>
            </Box>
            <Box>
              <LineChart
                xAxis={[
                  {
                    scaleType: 'band',
                    data: Object.keys(obj?.dates),
                    tickLabelStyle: {
                      angle: 90,
                      textAnchor: 'start',
                      fontSize: 15,
                      fontWeight: 600,
                    },
                  },
                ]}
                yAxis={[
                  {
                    data: Object.values(obj?.dates),
                    tickLabelStyle: { textAnchor: 'end', fontSize: 15, fontWeight: 600 },
                  },
                ]}
                series={[{ data: Object.values(obj?.dates), color: '#DE196B' }]}
                width={600}
                height={400}
                margin={{ bottom: 100 }}
              />
              <Typography align="center">Количество запросов в день</Typography>
            </Box>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default Dashboard;
