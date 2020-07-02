export default $axios => resource => ({
  get (packageId) {
    return $axios.$get(`${resource}/${packageId}/`)
  },
  create (packageId, payload) {
    return $axios.$post(`${resource}/${packageId}/`, payload)
  },
  getFileComment (packageId, fileId) {
    return $axios.$get(`${resource}/${packageId}/file/${fileId}/`)
  },
  createFileComment (packageId, fileId, payload) {
    return $axios.$post(`${resource}/${packageId}/file/${fileId}/`, payload)
  }
})
