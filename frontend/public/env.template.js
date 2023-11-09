(function (window) {
    window.env = window.env || {};

    // Environment variables
    window["env"]["backendUrl"] = "${BACKEND_URL}";
    window["env"]["frontendUrl"] = "${FRONTEND_URL}";
    window["env"]["msalClientId"] = "${MSAL_CLIENT_ID}";
    window["env"]["msalAuthority"] = "${MSAL_AUTHORITY}";
})(this);