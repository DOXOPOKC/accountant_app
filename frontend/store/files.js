export const types = {
  SET_FILES: 'SET_FILES',
  FETCH_FILES: 'FETCH_FILES',

  SET_FILE: 'SET_FILE',
  CREATE_FILE: 'CREATE_FILE',
  UPDATE_FILE: 'UPDATE_FILE',
  DELETE_FILE: 'DELETE_FILE'
}

export const state = () => ({
  list: [],
  detail: {}
})

export const mutations = {
  [types.SET_FILES] (state, files) {
    state.list = files
  },
  [types.SET_FILE] (state, file) {
    state.detail = file
  }
}

export const actions = {
  // Возвращает список файлов
  async [types.FETCH_FILES] ({ commit }, { contragentId, packageId }) {
    const data = await this.$repositories.files.get(contragentId, packageId)
    commit(types.SET_FILES, data)
  },
  // Добавление нового файла
  async [types.CREATE_FILE] ({ commit, dispatch }, { vueFileAgent, contragentId, packageId }) {
    try {
      const formData = new FormData()
      formData.append('file', vueFileAgent.filesData[0].file)
      formData.append('filename', vueFileAgent.filesData[0].file.name)
      formData.append('package_id', packageId)
      await this.$repositories.files.create(contragentId, packageId, formData)
      dispatch(types.FETCH_FILES, { contragentId, packageId })
      this.$toast.success('Файл успешно добавлен')
    } catch (error) {
      this.$toast.error('Ошибка! Некорректный файл')
    }
  },
  async [types.DELETE_FILE] ({ commit, dispatch }, { contragentId, packageId, fileId }) {
    try {
      await this.$repositories.files.delete(contragentId, packageId, fileId)
      dispatch(types.FETCH_FILES, { contragentId, packageId })
      this.$toast.success('Файл успешно удален')
    } catch (error) {
      this.$toast.error('Ошибка!')
    }
  }
}

export const getters = {}
