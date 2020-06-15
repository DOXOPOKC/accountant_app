const strategy = 'local'
const FALLBACK_INTERVAL = 180000

async function refreshTokenF ($auth, $axios, token, refreshToken, store, redirect) {
  if (refreshToken) {
    try {
      const response = await $axios.post('user/login/refresh/', { refresh: refreshToken })
      token = response.data.access
      refreshToken = response.data.refresh || refreshToken
      $axios.setToken(token, 'Bearer')
      $auth.setToken('local', 'Bearer ' + token)
      $auth.setRefreshToken(strategy, refreshToken)
      return decodeToken.call(this, token).exp
    } catch (error) {
      $auth.logout()
      redirect('/login')
      throw new Error('Error refreshing token')
    }
  }
}

export default function ({ app, store, redirect }) {
  const { $axios, $auth } = app
  let token
  let refreshToken

  $axios.onError(async (err) => {
    if (!err.config.retry && err.response.status === 401) {
      err.config.retry = true
      token = $auth.getToken(strategy)
      refreshToken = $auth.getRefreshToken(strategy)
      if (refreshToken) {
        await refreshTokenF($auth, $axios, token, refreshToken, store, redirect)
        err.config.headers = $axios.defaults.headers.common
        return $axios(err.config)
      } else {
        $auth.logout()
        redirect('/login')
      }
    } else {
      redirect('/')
    }
    return Promise.reject(err)
  })

  setInterval(async function () {
    token = $auth.getToken(strategy)
    refreshToken = $auth.getRefreshToken(strategy)
    await refreshTokenF($auth, $axios, token, refreshToken, store, redirect)
  }, FALLBACK_INTERVAL)
}

function decodeToken (str) {
  str = str.split('.')[1]
  str = str.replace('/-/g', '+')
  str = str.replace('/_/g', '/')
  switch (str.length % 4) {
    case 0:
      break
    case 2:
      str += '=='
      break
    case 3:
      str += '='
      break
    default:
      throw new Error('Invalid token')
  }
  str = (str + '===').slice(0, str.length + (str.length % 4))
  str = str.replace(/-/g, '+').replace(/_/g, '/')
  str = decodeURIComponent(escape(Buffer.from(str, 'base64').toString('binary')))
  str = JSON.parse(str)
  return str
}
