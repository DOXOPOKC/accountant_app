export const types = {
  SET_PACKAGES: 'SET_PACKAGES',
  FETCH_PACKAGES: 'FETCH_PACKAGES',

  SET_PACKAGE: 'SET_PACKAGE',
  FETCH_PACKAGE: 'FETCH_PACKAGE'
}

export const state = () => ({
  list: [],
  detail: {}
})

export const mutations = {
  [types.SET_CONTRAGENTS] (state, contragents) {
    state.list = contragents
  },
  [types.SET_CONTRAGENT] (state, contragent) {
    state.detail = contragent
  }
}

export const actions = {
  // Возвращает список пакетов с документами конкретного контрагента
  // async [types.FETCH_CONTRAGENTS] (store, id) {
  //     const data = await this.$axios.$get(`http://localhost/api/contragents/${id}/packages`)
  //     store.commit(types.SET_CONTRAGENTS, data)
  // },
  // // Генерация пакета (создание нового)
  // async [types.FETCH_CONTRAGENTS] (store, id) {
  //     const data = await this.$axios.$post(`http://localhost/api/contragents/${id}/packages`)
  //     store.commit(types.SET_CONTRAGENTS, data)
  // },
  // // Содержимое пакета
  // async [types.FETCH_CONTRAGENTS] (store, id, packageId) {
  //     const data = await this.$axios.$get(`http://localhost/api/contragents/${id}/packages/${packageId}`)
  //     store.commit(types.SET_CONTRAGENTS, data)
  // },
  // // Перегенирация
  // async [types.FETCH_CONTRAGENTS] (store, id, packageId) {
  //     const data = await this.$axios.$put(`http://localhost/api/contragents/${id}/packages/${packageId}`)
  //     store.commit(types.SET_CONTRAGENTS, data)
  // },
  // // Статус пакета переводится в закрытый
  // async [types.FETCH_CONTRAGENTS] (store, id) {
  //     const data = await this.$axios.$delete(`http://localhost/api/contragents/${id}/packages`)
  //     store.commit(types.SET_CONTRAGENTS, data)
  // }
}

export const getters = {}
