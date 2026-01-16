const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
})


// module.exports = defineConfig({
//   transpileDependencies: true,
//   devServer: {
//     allowedHosts: 'all',
//     hot: false,
//     liveReload: false,
//     proxy: {
//       '/api': {
//         target: 'http://127.0.0.1:8000/',
//         changeOrigin: true
//       }
//     },
//     client: {
//       webSocketURL: {
//         protocol: 'wss',
//         hostname: '0.0.0.0',
//         port: 443
//       }
//     }
//   }
// })

