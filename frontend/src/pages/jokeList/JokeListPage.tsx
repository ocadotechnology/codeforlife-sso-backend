import React from 'react';

import JokeList from '../../features/jokeList/JokeList';

import { SayHello } from 'codeforlife';

export default function JokeListPage(): JSX.Element {
  return (
    <div style={{ backgroundColor: 'lightblue' }}>
      <JokeList />
      <SayHello name="Stefan" />
    </div>
  );
}
