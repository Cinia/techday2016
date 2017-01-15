# robot-ui

Web UI for the tech day robot project.

## Setting up

Requirements:
- Node.js 4+
- Basic C/C++ build tools for library deps

Install dependencies with `npm i`.

Copy `app/config.js.dist` to `app/config.js` and configure the robot server URLs.

You can start a dev environment that automatically reloads on changes with `npm run start`.

To build a "production" version that can be deployed as static web content, run `npm run build`. You can start a minimal Express server to test this build with `npm run server`.
