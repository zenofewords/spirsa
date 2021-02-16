const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const WebpackBundleTracker = require('webpack-bundle-tracker')

module.exports = {
  mode: 'production',
  entry: {
    base: './static/javascript/base',
    contact: './static/javascript/contact',
    art: './static/javascript/art',
  },
  output: {
    filename: '[name]_[contenthash].js',
    path: path.resolve(__dirname, 'staticfiles/bundles'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          }
        },
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ]
      },
      {
        test: /\.(woff(2)?)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/'
            }
          }
        ]
      },
    ]
  },
  plugins: [
    new WebpackBundleTracker({
      filename: './webpack-stats-prod.json',
    }),
    new MiniCssExtractPlugin({
      filename: '[name]_[contenthash].css',
    }),
    new CleanWebpackPlugin(),
  ],
}
