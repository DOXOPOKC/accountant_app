export default $axios => resource => ({
  get () {
    return $axios.$get(`${resource}/`)
  },
  getContragent (id) {
    return $axios.$get(`${resource}/${id}/`)
  },
  create (payload) {
    return $axios.$post(`${resource}/`, payload)
  },
  update (payload, id) {
    return $axios.$put(`${resource}/${id}/`, payload)
  },
  updateContract (payload, id) {
    return $axios.$put(`${resource}/${id}/contract/`, payload)
  },
  delete (id) {
    return $axios.$delete(`${resource}/${id}/`)
  }
})
