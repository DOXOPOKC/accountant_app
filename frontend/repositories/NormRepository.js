export default $axios => resource => ({
  get () {
    return $axios.$get(`${resource}/`)
  }
})
