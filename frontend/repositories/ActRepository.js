export default $axios => resource => ({
  // Создание акта
  create (contragentId, packageId, payload) {
    return $axios.$post(`${resource}/${contragentId}/packages/${packageId}/act/`, payload)
  },
  // Обновление акта
  update (contragentId, packageId, payload) {
    return $axios.$patch(`${resource}/${contragentId}/packages/${packageId}/act/`, payload)
  }
})
