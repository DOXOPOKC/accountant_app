import Repository from '~/repositories/RepositoryFactory'

const contragentRepository = Repository.get('contragents')

export const types = {
  SET_CONTRAGENTS: 'SET_CONTRAGENTS',
  FETCH_CONTRAGENTS: 'FETCH_CONTRAGENTS',

  SET_CONTRAGENT: 'SET_CONTRAGENT',
  FETCH_CONTRAGENT: 'FETCH_CONTRAGENT'
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
  async [types.FETCH_CONTRAGENT] ({ commit }, id) {
    const { data } = await contragentRepository.getContragent(id)
    commit(types.SET_CONTRAGENT, data)
  },
  async [types.FETCH_CONTRAGENTS] ({ commit }) {
    const { data } = await contragentRepository.get()
    commit(types.SET_CONTRAGENTS, data)
  }
}

export const getters = {}
