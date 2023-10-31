import * as React from "react";
import { Admin, Resource, Layout } from "react-admin";
import { BrowserRouter } from "react-router-dom";
import { LoginPage } from "ra-auth-msal";

import customDataProvider from "./data/customDataProvider";
import { theme } from "./themes/theme";
import { BeATAppbar } from "./appbar/Appbar";

import { DecisionList } from "./components/decision/DecisionList";
import { DecisionShow } from "./components/decision/DecisionShow";
import { AnnotationCreate } from "./components/annotation/AnnotationCreate";
import { authProvider, msalobj } from "./authorization/authProvider";
const BeATLayout = (props) => <Layout {...props} appBar={BeATAppbar} />;

const App = () => {
  const wrappedAcquireTokenSilent = () =>
    msalobj
      .acquireTokenSilent({
        scopes: [`${import.meta.env.VITE_MSAL_CLIENT_ID}/.default`],
        account: msalobj.getActiveAccount(),
      })
      .then((response) => response?.accessToken);

  const dataProvider = customDataProvider(wrappedAcquireTokenSilent);

  return (
    <BrowserRouter>
      <Admin
        dataProvider={dataProvider}
        theme={theme}
        layout={BeATLayout}
        authProvider={authProvider}
        loginPage={LoginPage}
      >
        <Resource
          name="decisions"
          list={DecisionList}
          show={DecisionShow}
          recordRepresentation="name"
        />
        <Resource name="taxonomies" recordRepresentation="name" />
        <Resource
          name="annotations"
          create={AnnotationCreate}
          recordRepresentation="id"
        />
      </Admin>
    </BrowserRouter>
  );
};

export default App;
