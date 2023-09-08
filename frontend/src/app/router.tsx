import React from 'react';
import { createBrowserRouter } from 'react-router-dom';

import JokeListPage from '../pages/jokeList/JokeListPage';
import CreateReactAppPage from '../pages/createReactApp/CreateReactAppPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <JokeListPage />
  },
  {
    path: '/create-react-app',
    element: <CreateReactAppPage />
  }
]);

export default router;
