import api from '../../app/api';
import { Joke } from './jokeListSlice';

const jokeListApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getRandomJoke: builder.query<Joke, void>({
      query: () => 'random_joke'
    })
  })
});

export default jokeListApi;
export const {
  useGetRandomJokeQuery,
  useLazyGetRandomJokeQuery
} = jokeListApi;
