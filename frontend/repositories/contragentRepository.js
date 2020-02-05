import client from './clients/axiosClient'

const resource = '/api/contragents'

export default {
  get () {
    return client.get(`${resource}`)
  },
  getPost (id) {
    return client.get(`${resource}/${id}`)
  },
  create (payload) {
    return client.post(`${resource}`, payload)
  },
  update (payload, id) {
    return client.put(`${resource}/${id}`, payload)
  },
  delete (id) {
    return client.delete(`${resource}/${id}`)
  }
}
