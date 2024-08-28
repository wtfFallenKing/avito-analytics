import React from 'react';
import { Datagrid, DateField, FunctionField, List, NumberField } from 'react-admin';

function StorageLogsList() {
  return (
    <List>
      <Datagrid bulkActionButtons={false}>
        <NumberField source="id" />
        <DateField source="happened_at" showTime />
        <NumberField source="baseline" />
        <FunctionField
          source="discounts"
          render={(e) => {
            return e.discounts.join(', ');
          }}
        />
      </Datagrid>
    </List>
  );
}

export default StorageLogsList;
