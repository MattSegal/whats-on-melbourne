const path = require('path')
const webpack = require('webpack')
const TerserPlugin = require('terser-webpack-plugin')

const baseConfig = require('./webpack.base.js')

module.exports = {
  ...baseConfig,
  mode: 'production',
  output: {
    path: __dirname + '/dist/build',
    filename: 'main.js',
  },
  optimization: {
    minimizer: [new TerserPlugin()],
  },
  plugins: [
    ...baseConfig.plugins,
    new webpack.DefinePlugin({
      // Build system envars
      SERVER: JSON.stringify('https://api.whatsonmelb.fun'),
      MAPS_API_KEY: JSON.stringify('AIzaSyAODQvpxFVBugCvwd2aXcPyLA_XTBft_hA'),
    }),
  ],
}
