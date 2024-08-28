import React from 'react';
import { Menu } from 'react-admin';

function CustomMenu() {
  return (
    <Menu>
      <Menu.DashboardItem />
      <Menu.ResourceItem name="matrix" />
      <Menu.ResourceItem name="location" />
      <Menu.ResourceItem name="category" />
      <Menu.ResourceItem name="storage_logs" />
      <Menu.ResourceItem name="matrix_logs" />
    </Menu>
  );
}

export default CustomMenu;
