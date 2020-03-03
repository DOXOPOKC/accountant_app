import cookies from 'js-cookie'

export const state = () => ({
  access: null,
  refresh: null
})

export const mutations = {
  SET_TOKENS (state, { access, refresh }) {
    state.access = access
    state.refresh = refresh
  },
  REMOVE_TOKEN (state) {
    state.access = null
    state.refresh = null
  }
}

export const actions = {
  setToken ({ commit }, { access, refresh }) {
    this.$axios.setToken(access, 'Bearer')
    const expiryTime = new Date(new Date().getTime() + 10000)
    cookies.set('x-access-token', access, { expires: expiryTime })
    commit('SET_TOKEN', { access, refresh })
  },
  async refreshToken ({ dispatch, store }) {
    const { refresh } = await this.$axios.$post('user/login/refresh/', store.refresh)
    dispatch('setToken', { refresh })
  },
  async login ({ dispatch }) {
    const { access, refresh } = await this.$axios.$post('user/login/')
    dispatch('setToken', { access, refresh })
  },
  logout ({ commit }) {
    this.$axios.setToken(false)
    cookies.remove('x-access-token')
    commit('REMOVE_TOKEN')
  }
}
