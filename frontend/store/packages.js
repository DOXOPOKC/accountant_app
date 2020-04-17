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
    const data = await this.$repositories.packages.get(id)
    commit(types.SET_PACKAGES, data)
  },
  // // Генерация пакета (создание нового)
  async [types.GENERATE_PACKAGE] ({ commit, dispatch, rootState }) {
    try {
      const data = await this.$repositories.packages.create(rootState.contragents.detail.id, rootState.contragents.detail)
      this.commit('tasks/SET_TASK', data)
      this.$toast.success('Пакет успешно сгенерирован')
    } catch (error) {
      this.$toast.error('Ошибка! Есть активный пакет')
    }
  },
  // // Содержимое пакета
  async [types.FETCH_PACKAGE] ({ commit }, { contragentId, packageId }) {
    try {
      const data = await this.$repositories.packages.getPackage(contragentId, packageId)
      commit(types.SET_PACKAGE, data)
      this.commit('tasks/SET_TASK', data.name_uuid)
      this.dispatch('tasks/FETCH_TASKS', { contragentId, packageId })
    } catch (error) {
      this.$toast.error('Ошибка при загрузке пакета!')
    }
  },
  // Перегенирация
  async [types.REGENERATE_PACKAGE] ({ dispatch }, { contragentId, packageId }) {
    try {
      await this.$repositories.packages.update(contragentId, packageId)
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
      this.$toast.success('Пакет успешно перегенерирован')
    } catch (error) {
      this.$toast.error('Ошибка генерации')
    }
  },
  // Статус пакета переводится в закрытый
  async [types.DEACTIVATE_PACKAGE] ({ dispatch }, { contragentId, packageId }) {
    try {
      await this.$repositories.packages.delete(contragentId, packageId)
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
      this.$toast.error('Пакет неактивен')
    } catch (error) {
      this.$toast.error('Ошибка статуса')
    }
  }
}

export const getters = {}
