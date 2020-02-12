import client from '~/repositories/clients/AxiosClient'

export default {
  // Возвращает список пакетов с документами конкретного контрагента
  get (contragentId) {
    return client.get(`/api/contragents/${contragentId}/packages/`)
  },
  // Содержимое пакета
  getPackage (contragentId, packageId) {
    return client.get(`/api/contragents/${contragentId}/packages/${packageId}/`)
  },
  // Генерация пакета (создание нового)
  create (contragentId, payload) {
    return client.post(`/api/contragents/${contragentId}/packages/`, payload)
  },
  // Перегенирация
  update (contragentId, packageId, payload) {
    return client.put(`/api/contragents/${contragentId}/packages/${packageId}/`, payload)
  },
  // Статус пакета переводится в закрытый
  delete (contragentId, packageId) {
    return client.delete(`/api/contragents/${contragentId}/packages/${packageId}/`)
  }
}
