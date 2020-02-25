import Repository from '~/repositories/RepositoryFactory'

const contragentRepository = Repository.get('contragents')
const normsRepository = Repository.get('norms')
const signUsersRepository = Repository.get('signUsers')

export const types = {
  SET_CONTRAGENTS: 'SET_CONTRAGENTS',
  FETCH_CONTRAGENTS: 'FETCH_CONTRAGENTS',

  SET_CONTRAGENT: 'SET_CONTRAGENT',
  CREATE_CONTRAGENT: 'CREATE_CONTRAGENT',
  FETCH_CONTRAGENT: 'FETCH_CONTRAGENT',
  UPDATE_CONTRAGENT: 'UPDATE_CONTRAGENT',

  SET_NORM_LIST: 'SET_NORM_LIST',
  FETCH_NORM_LIST: 'FETCH_NORM_LIST',

  SET_SIGN_USERS_LIST: 'SET_SIGN_USERS_LIST',
  FETCH_SIGN_USERS_LIST: 'FETCH_SIGN_USERS_LIST'
}

export const state = () => ({
  normList: [],
  signUsers: [],
  list: [],
  detail: {}
})

export const mutations = {
  [types.SET_CONTRAGENT] (state, contragent) {
    state.detail = Object.assign({}, state.detail, contragent)
  },
  [types.SET_CONTRAGENTS] (state, contragents) {
    state.list = contragents
  },
  [types.SET_NORM_LIST] (state, normList) {
    state.normList = normList
  },
  [types.SET_SIGN_USERS_LIST] (state, signUsers) {
    state.signUsers = signUsers
  }
}

export const actions = {
  async [types.FETCH_CONTRAGENT] ({ commit }, id) {
    const { data } = await contragentRepository.getContragent(id)
    commit(types.SET_CONTRAGENT, data)
  },
  async [types.CREATE_CONTRAGENT] ({ dispatch }, { vueFileAgent }) {
    try {
      const formData = new FormData()
      formData.append('file', vueFileAgent.filesData[0].file)
      formData.append('filename', vueFileAgent.filesData[0].file.name)
      await contragentRepository.create(formData)
      dispatch(types.FETCH_CONTRAGENTS)
      this.$toast.success('Контрагент успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.FETCH_CONTRAGENTS] ({ commit }) {
    const { data } = await contragentRepository.get()
    commit(types.SET_CONTRAGENTS, data)
  },
  async [types.UPDATE_CONTRAGENT] ({ state, commit }) {
    try {
      const { data } = await contragentRepository.update(state.detail, state.detail.id)
      commit(types.SET_CONTRAGENT, data)
      this.$toast.success('Контрагент сохранен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.FETCH_NORM_LIST] ({ commit }) {
    const { data } = await normsRepository.get()
    commit(types.SET_NORM_LIST, data)
  },
  async [types.FETCH_SIGN_USERS_LIST] ({ commit }) {
    const { data } = await signUsersRepository.get()
    commit(types.SET_SIGN_USERS_LIST, data)
  }
}

export const getters = {}
