import React from 'react';
import { Layout, LayoutProps } from 'react-admin';
import CustomMenu from './menu';
import { Appbar } from './Appbar';

const CustomLayout = (props: LayoutProps) => <Layout {...props} menu={CustomMenu} appBar={Appbar} />;

export default CustomLayout;