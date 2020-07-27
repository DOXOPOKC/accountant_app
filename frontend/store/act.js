export const types = {
  SET_ACT: 'SET_ACT',

  CREATE_ACT: 'CREATE_ACT',
  FETCH_ACT: 'FETCH_ACT'
}

export const state = () => ({
  detail: {
    date: '',
    time: '',
    act_number: '',
    by_plan: false,
    by_phys: false,
    phys_data: '',
    by_jur: false,
    jur_data: '',
    address: '',
    exam_descr: '',
    evidence: '',
    add_info: '',
    exam_result: '',
    photos: []
  }
})

export const mutations = {
  [types.SET_ACT] (state, act) {
    console.log(Object.assign({}, state.detail, act), 'act store')
    state.detail = Object.assign({}, state.detail, act)
  }
}

export const actions = {
  async [types.FETCH_ACT] ({ dispatch, state }, { contragentId, packageId }) {
    try {
      await this.$repositories.act.update(contragentId, packageId, {})
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.CREATE_ACT] ({ dispatch, state }, { contragentId, packageId }) {
    try {
      await this.$repositories.act.create(contragentId, packageId, state.detail)
      await dispatch(types.FETCH_ACT, { contragentId, packageId })
      this.$toast.success('Акт успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  }
}

export const getters = {}
