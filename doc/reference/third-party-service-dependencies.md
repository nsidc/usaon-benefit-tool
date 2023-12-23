---
title: "Third party services"
---

## Google SSO

A Google OAuth application is required for login to work. Our app requires a client ID
and client secret to communicate with the Google OAuth application.


### Initial setup

_TODO_


### Redirect URIs

> :warning: This configuration needs to be updated for every unique deployment URL of
> this app.

Our app's deployed URIs also must be registered with Google as ["Authorized redirect
URIs"](https://console.cloud.google.com/apis/credentials) (from the link, click on your
app under the "OAuth 2.0 Client IDs" section). The following URIs should be provided for
local development:

* `http://localhost:5000/google_oauth/google/authorized`
* `http://127.0.0.1:5000/google_oauth/google/authorized`

Add more URIs (substituting the protocol, hostname, and port number, and nothing else)
for each separate deployment.
