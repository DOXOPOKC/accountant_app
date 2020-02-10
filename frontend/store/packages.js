import Repository from '~/repositories/RepositoryFactory'

const packageRepository = Repository.get('packages')

export const types = {
  SET_PACKAGES: 'SET_PACKAGES',
  FETCH_PACKAGES: 'FETCH_PACKAGES',

  SET_PACKAGE: 'SET_PACKAGE',
  FETCH_PACKAGE: 'FETCH_PACKAGE',

  GENERATE_PACKAGE: 'GENERATE_PACKAGE',
  REGENERATE_PACKAGE: 'REGENERATE_PACKAGE'
}

export const state = () => ({
  list: [],
  detail: {}
})

// to="put /contragents/{id}/packages/{package_id}"
// )
// | Перегенерировать

// to="post /contragents/{id}/packages/{package_id}"
// )
// | Сгенерировать пакет

export const mutations = {
  [types.SET_PACKAGES] (state, contragentPackages) {
    state.list = contragentPackages
  },
  [types.SET_PACKAGE] (state, contragentPackage) {
    state.detail = contragentPackage
  }
}

export const actions = {
  // Возвращает список пакетов с документами конкретного контрагента
  async [types.FETCH_PACKAGES] ({ commit }, id) {
    const { data } = await packageRepository.get(id)
    commit(types.SET_PACKAGES, data)
  },
  // // Генерация пакета (создание нового)
  async [types.GENERATE_PACKAGE] ({ commit, rootState }) {
    const { data } = await packageRepository.create(rootState.contragents.detail.id, rootState.contragents.detail)
    commit(types.SET_PACKAGE, data)
  },
  // // Содержимое пакета
  async [types.FETCH_PACKAGE] ({ commit }, { contragentId, packageId }) {
    const { data } = await packageRepository.getPackage(contragentId, packageId)
    commit(types.SET_PACKAGE, data)
  }
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
