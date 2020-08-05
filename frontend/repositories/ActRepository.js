export default $axios => resource => ({
  // Создание акта
  create (contragentId, packageId, payload) {
    return $axios.$post(`${resource}/${contragentId}/packages/${packageId}/act/`, payload, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  // Обновление акта
  update (contragentId, packageId, payload) {
    return $axios.$patch(`${resource}/${contragentId}/packages/${packageId}/act/`, payload, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
})
