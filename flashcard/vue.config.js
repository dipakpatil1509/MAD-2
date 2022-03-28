module.exports = {
    publicPath:"/app/",
    pwa: {
        // configure the workbox plugin
        workboxPluginMode: 'InjectManifest',
        workboxOptions: {
          swSrc: 'src/service-worker.js',
          swDest: 'service-worker.js',
        }
    }
}