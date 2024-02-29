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
  const msalEnabled = "msalEnabled" in window["env"] ? Boolean(Number(window["env"]["msalEnabled"])) : true

  const wrappedAcquireTokenSilent = () =>
    msalobj
      .acquireTokenSilent({
        scopes: [`${window["env"]["msalClientId"]}/.default`],
        account: msalobj.getActiveAccount(),
      })
      .then((response) => response?.accessToken);

  const dataProvider = customDataProvider(msalEnabled ? wrappedAcquireTokenSilent : () => {return Promise.resolve("")});

  return (
    <BrowserRouter>
      <Admin
        dataProvider={dataProvider}
        theme={theme}
        layout={BeATLayout}
        authProvider={msalEnabled ? authProvider : undefined}
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
