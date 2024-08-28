import polyglotI18nProvider from 'ra-i18n-polyglot';
import russianMessages from 'ra-language-russian';

const ru = {
  ...russianMessages,
  resources: {
    location: {
      name: 'Локации',
      fields: {
        name: 'Название региона',
        parent_id: 'Вышестоящий регион',
      },
    },
    category: {
      name: 'Категории',
      fields: {
        name: 'Название категории',
        parent_id: 'Вышестоящая категория',
      },
    },
    matrix: {
      name: 'Матрицы цен',
      fields: {
        name: 'Имя',
        type: 'Тип',
        segment_id: 'Сегмент',
      },
    },
    price: {
      fields: {
        matrix_id: 'Матрица',
        category_id: 'Категория',
        location_id: 'Регион',
        price: 'Цена',
      },
    },
    storage_logs: {
      name: 'Логи Storage',
      fields: {
        happened_at: 'Время',
      },
    },
    matrix_logs: {
      name: 'Логи матриц',
      fields: {
        matrix: 'Матрица',
        type: 'Действие',
        happened_at: 'Время',
      },
    },
  },
};

export const i18nProvider = polyglotI18nProvider(() => ru, 'ru');
