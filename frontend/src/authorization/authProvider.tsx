import { msalAuthProvider } from "ra-auth-msal";
import { PublicClientApplication } from "@azure/msal-browser";
import { msalConfig, getIdentityFromAccount } from "./authConfig";

export const msalobj = new PublicClientApplication(msalConfig);

export const authProvider = msalAuthProvider({
  msalInstance: msalobj,
  getIdentityFromAccount,
});
