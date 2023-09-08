import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://official-joke-api.appspot.com/'
  }),
  endpoints: () => ({})
});

export default api;
