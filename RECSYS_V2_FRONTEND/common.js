// Shared helper for pages that require the user to be logged in
// (UserHome.html, AdminHome.html, ResearcherHome.html).
//
// Wraps fetch() and sends the browser to the login page whenever the
// backend says the caller isn't authenticated (401 - e.g. RBAC() rejecting
// an expired or invalid JWT). Use this instead of the raw fetch() for any
// call to an endpoint that requires being logged in.
//
// Included as a plain <script src="../common.js"></script> tag rather than
// an ES module, to match how the rest of this project's frontend is built
// (no bundler/build step) - so authFetch is just a normal global function.
async function authFetch(url, options = {}) {
  const response = await fetch(url, { credentials: "include", ...options });

  if (response.status === 401) {
    window.location.href = "../login.html";
    // Stop here rather than letting the caller's code run against this
    // response (e.g. `await response.json()`) - the page is navigating
    // away, so nothing after this needs to resolve.
    return new Promise(() => {});
  }

  return response;
}
