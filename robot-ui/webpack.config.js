var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');

var DEV_MODE = process.env.NODE_ENV === 'dev';

var plugins = [
    new webpack.optimize.CommonsChunkPlugin({
        // chunk name to generate
        name: 'vendor',
        // chunk naming pattern
        filename: 'vendor.[chunkhash].js'
    }),
    new HtmlWebpackPlugin({
        template: './index.template.ejs'
    })
];

var webpackConfig = {
    entry: {
        // our entry point
        app: './index.js',
        // bundle these separately to keep app clean
        vendor: [ 'react', 'react-dom' ]
    },
    devtool: 'source-map',
    output: {
        path: path.resolve('./target'),
        filename: '[name].[chunkhash].js',
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                // Windows pls
                exclude: /node_modules[\/\\]/,
                loader: 'babel-loader',
                query: {
                    plugins: ['babel-plugin-transform-class-properties'],
                    presets: [
                        ['es2015', {
                            modules: false
                        }],
                        'react'
                    ],
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: function(path) {
                    return path.match(/node_modules[\/\\]/);
                },
                query: {
                    presets: [
                        ['babel-preset-es2015', { modules: false }]
                    ],
                }
            },
            {
                test: /\.scss$/,
                loaders: ['style-loader', 'css-loader', 'sass-loader'],
            },
            {
                test: /\.css$/,
                loaders: ['style-loader', 'css-loader' ],
            },
            {
                test: /[\/\\]images[\/\\].+?\.svg$/,
                loader: 'url-loader?name=images/[hash].[ext]&limit=10000?mimetype=image/svg+xml'
            },
            {
                test: /[\/\\]images[\/\\].+?\.png$/,
                loader: 'url-loader?name=images/[hash].[ext]&limit=10000?mimetype=image/png'
            },
        ]
    },
    plugins: DEV_MODE ? plugins : plugins.concat([
        new webpack.optimize.UglifyJsPlugin({
            mangle: true,
            compress: {
                warnings: false
            },
        })
    ])
};

module.exports = webpackConfig;
