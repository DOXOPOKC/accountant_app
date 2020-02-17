import client from './clients/AxiosClient'

const resource = '/api/sign_users'

export default {
  get () {
    return client.get(`${resource}/`)
  }
}
