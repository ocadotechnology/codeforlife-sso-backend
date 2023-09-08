import { createTheme } from '@mui/material/styles';
import { orange } from '@mui/material/colors';
import { theme as baseTheme } from 'codeforlife';

// One of theme changes here.
const theme = createTheme(baseTheme, {
  palette: {
    primary: {
      main: orange.A700
    }
  }
});

export default theme;
