export default $axios => resource => ({
  get (taskId) {
    return $axios.$get(`${resource}/${taskId}/`)
  }
})
