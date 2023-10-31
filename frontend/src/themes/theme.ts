// In theme.js
import { defaultTheme } from "react-admin";
import { createTheme } from "@mui/material/styles";
import merge from "lodash/merge";

export const theme = createTheme(
  merge({}, defaultTheme, {
    palette: {
      primary: {
        main: "#009de0",
      },
      secondary: {
        main: "#003066",
      },
      background: {
        default: "#f6f6f6",
        paper: "#fafafa",
      },
    },
    typography: {
      fontFamily: "Roboto",
    },
  })
);
