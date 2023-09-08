import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { type RootState } from '../../app/store';
import jokeListApi from './jokeListAPI';

export interface Joke {
  id: number,
  type: string,
  setup: string,
  punchline: string
}

export interface JokeListState {
  jokes: Joke[];
  status: 'idle' | 'loading' | 'failed';
}

const initialState: JokeListState = {
  jokes: [],
  status: 'idle'
};

export const jokeListSlice = createSlice({
  name: 'jokeList',
  initialState,
  reducers: {
    addJoke: (state, action: PayloadAction<{ setup: string, punchline: string }>) => {
      const joke: Joke = {
        ...action.payload,
        id: state.jokes.length * -1,
        type: 'general'
      };
      state.jokes.push(joke);
    }
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(jokeListApi.endpoints.getRandomJoke.matchPending, (state) => {
        state.status = 'loading';
      })
      .addMatcher(jokeListApi.endpoints.getRandomJoke.matchFulfilled, (state, action) => {
        state.status = 'idle';
        state.jokes.push(action.payload);
      })
      .addMatcher(jokeListApi.endpoints.getRandomJoke.matchRejected, (state) => {
        state.status = 'failed';
      });
  }
});

export const { addJoke } = jokeListSlice.actions;

export const selectJokes = (state: RootState): Joke[] => state.jokeList.jokes;

export default jokeListSlice.reducer;
