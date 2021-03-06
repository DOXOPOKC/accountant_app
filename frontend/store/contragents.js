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
  FETCH_SIGN_USERS_LIST: 'FETCH_SIGN_USERS_LIST',

  UPDATE_CONTRACT: 'UPDATE_CONTRACT',

  SET_GENERATE_FLAG: 'SET_GENERATE_FLAG'
}

export const state = () => ({
  canGenerate: false,
  normList: [],
  signUsers: [],
  list: [
    {
      contragent_class: '',
      debt: null,
      debt_period: null,
      excell_name: '',
      id: null,
      inn: null,
      klass: null,
      pack: null,
      physical_address: ''
    }
  ],
  detail: {
    is_func: false,
    class: null
  },
  excelTemplateLink: 'media/template.xlsx'
})

export const mutations = {
  [types.SET_GENERATE_FLAG] (state, flag) {
    state.canGenerate = flag
  },
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
    const data = await this.$repositories.contragents.getContragent(id)
    const {
      stat_value: statValue,
      signed_user: signedUser,
      norm_value: normValue,
      current_contract_date: currentContractDate
    } = data
    const canGenerate = (statValue && signedUser && normValue && currentContractDate)
    if (data.other_files) { this.commit(types.SET_FILES, data.other_files) }
    if (canGenerate) { commit(types.SET_GENERATE_FLAG, true) }
    commit(types.SET_CONTRAGENT, data)
  },
  async [types.CREATE_CONTRAGENT] ({ dispatch }, { vueFileAgent, filesDataForUpload }) {
    try {
      const formData = new FormData()
      formData.append('file', filesDataForUpload.file)
      formData.append('filename', filesDataForUpload.name())
      await this.$repositories.contragents.create(formData)
      dispatch(types.FETCH_CONTRAGENTS)
      this.$toast.success('Контрагент успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.FETCH_CONTRAGENTS] ({ commit }) {
    const data = await this.$repositories.contragents.get()
    commit(types.SET_CONTRAGENTS, data)
  },
  async [types.UPDATE_CONTRAGENT] ({ state, commit }) {
    try {
      const data = await this.$repositories.contragents.update(state.detail, state.detail.id)
      commit(types.SET_CONTRAGENT, data)
      this.$toast.success('Контрагент сохранен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.UPDATE_CONTRACT] ({ state, dispatch }) {
    try {
      await this.$repositories.contragents.updateContract(state.detail.number_contract, state.detail.id)
      dispatch(types.FETCH_CONTRAGENT, state.detail.id)
      this.$toast.success('Контракт сохранен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.FETCH_NORM_LIST] ({ commit }) {
    const data = await this.$repositories.norms.get()
    commit(types.SET_NORM_LIST, data)
  },
  async [types.FETCH_SIGN_USERS_LIST] ({ commit }) {
    const data = await this.$repositories.signUsers.get()
    commit(types.SET_SIGN_USERS_LIST, data)
  }
}

export const getters = {}
