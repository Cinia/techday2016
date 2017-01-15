// Require the rest of the application as a chunk named 'app';
// This makes webpack generate a minimal loader JS that imports the chunk.
require.ensure([], function(require) {
    require('./app/index.jsx');
}, 'app');
