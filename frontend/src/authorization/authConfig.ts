import { Configuration } from "@azure/msal-browser";

export const msalConfig: Configuration = {
  auth: {
    // 'Application (client) ID' of app registration in Azure portal - this value is a GUID
    clientId: window["env"]["msalClientId"],
    // Full directory URL, in the form of https://login.microsoftonline.com/<tenant-id>
    authority: window["env"]["msalAuthority"],
    // Full redirect URL, in form of http://localhost:8080/auth-callback
    redirectUri: `${window["env"]["frontendUrl"]}/auth-callback`,
    // We need to disable this feature because it is already handled by react-admin, and would otherwise conflict
    navigateToLoginRequestUrl: false,
  },
  cache: {
    cacheLocation: "sessionStorage", // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
};

/**
 * Custom function to get the identity from the account info.
 */
export const getIdentityFromAccount = async (account) => {
  return {
    id: account?.localAccountId,
    fullName: account?.name,
  };
};
