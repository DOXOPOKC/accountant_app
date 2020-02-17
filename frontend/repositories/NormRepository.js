import client from './clients/AxiosClient'

const resource = '/api/norms'

export default {
  get () {
    return client.get(`${resource}/`)
  }
}
