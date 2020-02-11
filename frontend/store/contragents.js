import Repository from '~/repositories/RepositoryFactory'

const contragentRepository = Repository.get('contragents')

export const types = {
  SET_CONTRAGENTS: 'SET_CONTRAGENTS',
  FETCH_CONTRAGENTS: 'FETCH_CONTRAGENTS',

  SET_CONTRAGENT: 'SET_CONTRAGENT',
  CREATE_CONTRAGENT: 'CREATE_CONTRAGENT',
  FETCH_CONTRAGENT: 'FETCH_CONTRAGENT',
  UPDATE_CONTRAGENT: 'UPDATE_CONTRAGENT'
}

export const state = () => ({
  list: [],
  detail: {}
})

export const mutations = {
  [types.SET_CONTRAGENT] (state, contragent) {
    state.detail = contragent
  },
  [types.SET_CONTRAGENTS] (state, contragents) {
    state.list = contragents
  }
}

export const actions = {
  async [types.FETCH_CONTRAGENT] ({ commit }, id) {
    const { data } = await contragentRepository.getContragent(id)
    commit(types.SET_CONTRAGENT, data)
  },
  async [types.CREATE_CONTRAGENT] ({ commit, dispatch }, { vueFileAgent }) {
    const formData = new FormData()
    formData.append('file', vueFileAgent.filesData[0].file)
    formData.append('filename', vueFileAgent.filesData[0].file.name)
    await contragentRepository.create(formData)
  },
  async [types.FETCH_CONTRAGENTS] ({ commit }) {
    const { data } = await contragentRepository.get()
    commit(types.SET_CONTRAGENTS, data)
  },
  async [types.UPDATE_CONTRAGENT] ({ state, commit }) {
    const { data } = await contragentRepository.update(state.detail, state.detail.id)
    commit(types.SET_CONTRAGENT, data)
  }
}

export const getters = {}
