export default $axios => resource => ({
  // Возвращает список пакетов с документами конкретного контрагента
  get (contragentId) {
    return $axios.$get(`${resource}/${contragentId}/packages/`)
  },
  // Содержимое пакета
  getPackage (contragentId, packageId) {
    return $axios.$get(`${resource}/${contragentId}/packages/${packageId}/`)
  },
  // Генерация пакета (создание нового)
  create (contragentId, payload) {
    return $axios.$post(`${resource}/${contragentId}/packages/`, payload)
  },
  // Перегенирация
  update (contragentId, packageId) {
    return $axios.$put(`${resource}/${contragentId}/packages/${packageId}/`)
  },
  // Статус пакета переводится в закрытый
  delete (contragentId, packageId) {
    return $axios.$delete(`${resource}/${contragentId}/packages/${packageId}/`)
  }
})
