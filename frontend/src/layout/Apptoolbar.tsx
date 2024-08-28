import React from 'react';
import { LoadingIndicator } from 'react-admin';
import { ThemeSwapper } from '~/themes/themeSwapper';

export const AppToolbar = () => (
  <>
    <ThemeSwapper />
    <LoadingIndicator />
  </>
);