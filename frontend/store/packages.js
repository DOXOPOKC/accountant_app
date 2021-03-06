export const types = {
  SET_PACKAGES: 'SET_PACKAGES',
  FETCH_PACKAGES: 'FETCH_PACKAGES',

  SET_PACKAGE: 'SET_PACKAGE',
  FETCH_PACKAGE: 'FETCH_PACKAGE',
  GENERATE_PACKAGE: 'GENERATE_PACKAGE',
  DOWNLOAD_PACKAGE: 'DOWNLOAD_PACKAGE',
  REGENERATE_PACKAGE: 'REGENERATE_PACKAGE',
  SEND_EVENT: 'SEND_EVENT',

  UPDATE_PACKAGE: 'UPDATE_PACKAGE',
  SET_TAX: 'SET_TAX',

  SET_ACTIVE_FLAG: 'SET_ACTIVE_FLAG'
}

export const state = () => ({
  isActive: null,
  list: [],
  detail: {}
})

export const mutations = {
  [types.SET_ACTIVE_FLAG] (state, flag) {
    state.isActive = flag
  },
  [types.SET_PACKAGES] (state, contragentPackages) {
    state.list = contragentPackages
  },
  [types.SET_PACKAGE] (state, contragentPackage) {
    state.detail = Object.assign({}, state.detail, contragentPackage)
  },
  [types.SET_TAX] (state, taxCount) {
    state.detail.tax_count = taxCount
  }
}

export const actions = {
  // Возвращает список пакетов с документами конкретного контрагента
  async [types.FETCH_PACKAGES] ({ commit }, id) {
    const data = await this.$repositories.packages.get(id)
    const isActive = data.find(contragentPackage => contragentPackage.is_active === true) || {}
    if (isActive.is_active) {
      commit(types.SET_ACTIVE_FLAG, true)
    } else {
      commit(types.SET_ACTIVE_FLAG, false)
    }
    commit(types.SET_PACKAGES, data)
  },
  // // Генерация пакета (создание нового)
  async [types.GENERATE_PACKAGE] ({ commit, dispatch, rootState }) {
    try {
      const data = await this.$repositories.packages.create(rootState.contragents.detail.id, rootState.contragents.detail)
      dispatch(types.FETCH_PACKAGES, rootState.contragents.detail.id)
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
      this.dispatch('tasks/FETCH_TASKS', { contragentId, packageId, taskUid: data.name_uuid })
    } catch (error) {
      this.$toast.error(`${error.response.data} - ${error.response.status}`)
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
  // Обновление данных пакета
  async [types.UPDATE_PACKAGE] ({ dispatch, state }, { contragentId, packageId }) {
    try {
      console.log(contragentId, packageId)
      await this.$repositories.packages.updatePackageState(
        contragentId,
        packageId,
        {
          tax: state.detail.tax_count
        })
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
      this.$toast.success('Пакет успешно обновлен')
    } catch (error) {
      this.$toast.error('Ошибка генерации')
    }
  },
  // Статус пакета переводится в закрытый
  async [types.SEND_EVENT] ({ dispatch }, { contragentId, packageId, eventId }) {
    try {
      await this.$repositories.packages.delete(contragentId, packageId, { event: eventId })
      await dispatch(types.FETCH_PACKAGE, { contragentId, packageId })
    } catch (error) {
      this.$toast.error('Ошибка статуса')
    }
  },
  // Скачать zip пакет
  async [types.DOWNLOAD_PACKAGE] ({ dispatch }, { contragentId, packageId }) {
    try {
      const response = await this.$repositories.packages.download(contragentId, packageId)
      const blob = new Blob([response], { type: 'application/zip' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (error) {
      this.$toast.error('Ошибка скачивания')
    }
  }
}

export const getters = {}
