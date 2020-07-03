export const types = {
  SET_COMMENTS: 'SET_COMMENTS',
  CREATE_COMMENT: 'CREATE_COMMENT',
  FETCH_COMMENTS: 'FETCH_COMMENTS',

  CREATE_FILE_COMMENT: 'CREATE_FILE_COMMENT',
  FETCH_FILE_COMMENTS: 'FETCH_FILE_COMMENTS'
}

export const state = () => ({
  list: [],
  listFile: []
})

export const mutations = {
  [types.SET_COMMENTS] (state, comments) {
    state.list = comments
  }
}

export const actions = {
  async [types.FETCH_COMMENTS] ({ commit }, { packageId }) {
    const data = await this.$repositories.comments.get(packageId)
    commit(types.SET_COMMENTS, data)
  },
  async [types.CREATE_COMMENT] ({ dispatch, state }, { packageId, comment }) {
    try {
      await this.$repositories.comments.create(packageId, {
        user: this.state.auth.user.username,
        commentary_text: comment
      })
      await dispatch(types.FETCH_COMMENTS, { packageId })
      this.$toast.success('Комментарий успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.FETCH_FILE_COMMENTS] ({ commit }, { packageId, fileId }) {
    const data = await this.$repositories.comments.getFileComment(packageId, fileId)
    commit(types.SET_COMMENTS, data)
  },
  async [types.CREATE_FILE_COMMENT] ({ dispatch, state }, { fileId, packageId, comment }) {
    try {
      await this.$repositories.comments.createFileComment(packageId, fileId, {
        user: this.state.auth.user.username,
        commentary_text: comment
      })
      await dispatch(types.FETCH_FILE_COMMENTS, { packageId, fileId })
      this.$toast.success('Комментарий успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  }
}

export const getters = {}
