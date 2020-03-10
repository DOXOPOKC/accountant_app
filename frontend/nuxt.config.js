require('dotenv').config()

export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/static/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#2196f3', height: '4px' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~/plugins/vee-validate',
    // '~/plugins/i18n',
    '~/plugins/filters.js',
    '~/plugins/vue-file-agent',
    '~/plugins/repository',
    '~/plugins/axios'
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    '@nuxtjs/vuetify'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/toast',
    '@nuxtjs/dotenv'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: `${process.env.NUXT_ENV_PROTOCOL}://${process.env.NUXT_ENV_DOMAIN}/api`,
    credentials: true,
  },
  router: {
    middleware: ['loggedIn']
  },
  auth: {
    localStorage: false,
    cookie: {
      options: {
        expires: 7
      }
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: 'user/login/', method: 'post', propertyName: 'access' },
          logout: false,
          user: { url: 'user/', method: 'get', propertyName: false }
        },
        tokenRequired: true
      }
    },
    plugins: [{ src: '~/plugins/auth.js', mode: 'client' }]
  },
  /*
  ** Toats module
  ** See https://github.com/nuxt-community/modules/blob/master/packages/toast/README.md
  */
  toast: {
    position: 'bottom-right',
    duration: 3000,
    register: [
      // Register custom toasts
      {
        name: 'my-error',
        message: 'Oops...Something went wrong',
        options: {
          type: 'error'
        }
      }
    ]
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    optionsPath: '~/plugins/vuetify.options.js'
  },
  /*
  ** Build configuration
  */
  build: {
    transpile: ['vee-validate/dist/rules'],
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {}
  }
}
