import React, { useState } from 'react';
import Grid2 from '@mui/material/Unstable_Grid2';
import {
  List,
  ListItem,
  Button,
  TextField
} from '@mui/material/';

import { useAppSelector, useAppDispatch } from '../../app/hooks';
import { useLazyGetRandomJokeQuery } from './jokeListAPI';
import { selectJokes, addJoke } from './jokeListSlice';

export default function JokeList(): JSX.Element {
  const dispatch = useAppDispatch();
  const jokes = useAppSelector(selectJokes);
  const [setup, setSetup] = useState('');
  const [punchline, setPunchline] = useState('');
  const [lazyGetRandomJoke] = useLazyGetRandomJokeQuery();

  function handleSetupChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setSetup(event.target.value);
  }

  function handlePunchlineChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setPunchline(event.target.value);
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    dispatch(addJoke({ setup, punchline }));
  }

  function handleGetRandomJoke(): void {
    void lazyGetRandomJoke();
  }

  return (
    <Grid2 container spacing={2}>
      <Grid2 xs={12}>
        <List sx={{ width: '100%' }}>
          {jokes.map((joke) =>
            <ListItem key={joke.id}>{joke.setup} : {joke.punchline}</ListItem>
          )}
        </List>
      </Grid2>
      <Grid2 xsOffset={4} xs={4}>
        <Button
          sx={{ width: '100%' }}
          onClick={handleGetRandomJoke}
          style={{ marginBottom: '20px' }}>
          Get Random Joke
        </Button>
      </Grid2>
      <Grid2 container xs={12} spacing={1} >
        <form onSubmit={handleSubmit} style={{ width: '100%', height: '100%' }}>
          <Grid2 xsOffset={3} xs={6}>
            <TextField
              required
              id='setup'
              label='Setup'
              value={setup}
              onChange={handleSetupChange}
            />
          </Grid2>
          <Grid2 xsOffset={3} xs={6}>
            <TextField
              required
              id='punchline'
              label='Punchline'
              value={punchline}
              onChange={handlePunchlineChange}
            />
          </Grid2>
          <Grid2 xsOffset={5} xs={2}>
            <Button type='submit' sx={{ width: '100%' }}>
              Add Joke
            </Button>
          </Grid2>
        </form>
      </Grid2>
    </Grid2>
  );
}
