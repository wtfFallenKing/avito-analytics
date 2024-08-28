import React from 'react';
import { Datagrid, DateField, List, NumberField, SelectField } from 'react-admin';

function MatrixLogsList() {
  return (
    <List>
      <Datagrid bulkActionButtons={false}>
        <NumberField source="id" />
        <NumberField source="matrix_id" />
        <SelectField
          source="type"
          choices={[
            { id: 'CREATE', name: 'Создание' },
            { id: 'DELETE', name: 'Удаление' },
            { id: 'UPDATE', name: 'Изменение' },
          ]}
        />
        <DateField source="happened_at" showTime />
      </Datagrid>
    </List>
  );
}

export default MatrixLogsList;
