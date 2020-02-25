import Repository from '~/repositories/RepositoryFactory'

const packageRepository = Repository.get('packages')

export const types = {
  SET_PACKAGES: 'SET_PACKAGES',
  FETCH_PACKAGES: 'FETCH_PACKAGES',

  SET_PACKAGE: 'SET_PACKAGE',
  FETCH_PACKAGE: 'FETCH_PACKAGE',
  GENERATE_PACKAGE: 'GENERATE_PACKAGE',
  REGENERATE_PACKAGE: 'REGENERATE_PACKAGE',
  DEACTIVATE_PACKAGE: 'DEACTIVATE_PACKAGE'
}

export const state = () => ({
  list: [],
  detail: {}
})

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
  async [types.GENERATE_PACKAGE] ({ commit, dispatch, rootState }) {
    try {
      const { data } = await packageRepository.create(rootState.contragents.detail.id, rootState.contragents.detail)
      this.commit('tasks/SET_TASK', data)
      this.dispatch('tasks/FETCH_TASKS')
      this.$toast.success('Пакет успешно сгенерирован')
    } catch (error) {
      this.$toast.error('Ошибка! Есть активный пакет')
    }
  },
  // // Содержимое пакета
  async [types.FETCH_PACKAGE] ({ commit }, { contragentId, packageId }) {
    const { data } = await packageRepository.getPackage(contragentId, packageId)
    commit(types.SET_PACKAGE, data)
  },
  // Перегенирация
  async [types.REGENERATE_PACKAGE] ({ dispatch }, { contragentId, packageId }) {
    try {
      await packageRepository.update(contragentId, packageId)
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
      this.$toast.success('Пакет успешно перегенерирован')
    } catch (error) {
      this.$toast.error('Ошибка генерации')
    }
  },
  // Статус пакета переводится в закрытый
  async [types.DEACTIVATE_PACKAGE] ({ dispatch }, { contragentId, packageId }) {
    try {
      await packageRepository.delete(contragentId, packageId)
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
      this.$toast.error('Пакет неактивен')
    } catch (error) {
      this.$toast.error('Ошибка статуса')
    }
  }
}

export const getters = {}
