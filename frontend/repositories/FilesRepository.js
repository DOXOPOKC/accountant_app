export default $axios => resource => ({
  // Возвращает список файлов
  get (contragentId, packageId) {
    return $axios.$get(`${resource}/${contragentId}/packages/${packageId}/other-files/`)
  },
  // Содержимое файла
  getFile (contragentId, fileId, packageId) {
    return $axios.$get(`${resource}/${contragentId}/packages/${packageId}/other-files/${fileId}`)
  },
  // Добавление нового файла
  create (contragentId, packageId, payload) {
    return $axios.$post(`${resource}/${contragentId}/packages/${packageId}/other-files/`, payload)
  },
  // Обновления файла
  update (contragentId, packageId, fileId, payload) {
    return $axios.$put(`${resource}/${contragentId}/packages/${packageId}/other-files/${fileId}`, payload)
  },
  // Удаление файла
  delete (contragentId, packageId, fileId) {
    return $axios.$delete(`${resource}/${contragentId}/packages/${packageId}/other-files/${fileId}`)
  }
})
