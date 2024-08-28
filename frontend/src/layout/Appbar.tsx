import React from 'react';
import { AppBar } from 'react-admin';
import { AppToolbar } from './Apptoolbar';

export const Appbar = () => {
    return (
      <AppBar toolbar={<AppToolbar/>} />
  );
}