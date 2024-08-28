import React from 'react'
import { Show, SimpleShowLayout, TextField } from 'react-admin'

const LocationsShow = () => {
  return (
    <Show>
      <SimpleShowLayout>
        <TextField source="id" />
        <TextField source="key" />
        <TextField source="name" />
        <TextField source="parent_id" />
      </SimpleShowLayout>
    </Show>
  )
}

export default LocationsShow