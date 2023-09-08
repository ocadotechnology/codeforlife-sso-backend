import {
  configureStore,
  ThunkDispatch,
  ThunkAction,
  Action,
  AnyAction
} from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';

import api from '../app/api';
import counterReducer from '../features/counter/counterSlice';
import jokeListReducer from '../features/jokeList/jokeListSlice';

const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    counter: counterReducer,
    jokeList: jokeListReducer
  },
  middleware: (getDefaultMiddleware) => [
    ...getDefaultMiddleware(),
    api.middleware
  ]
});

setupListeners(store.dispatch);

export default store;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = ThunkDispatch<RootState, any, AnyAction>;
export type AppThunk<ReturnType = void> = ThunkAction<ReturnType, RootState, unknown, Action<string>>;
