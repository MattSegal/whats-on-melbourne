const path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: [
    './frontend/index.js'
  ],
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  plugins: [
    new BundleTracker({filename: 'webpack-stats.json'})
  ]
};
