export const types = {
  SET_ACT: 'SET_ACT',

  CREATE_ACT: 'CREATE_ACT',
  UPDATE_ACT: 'UPDATE_ACT'
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
    state.detail = Object.assign({}, state.detail, act)
  }
}

export const actions = {
  async [types.UPDATE_ACT] ({ dispatch, state }, { contragentId, packageId }) {
    try {
      const detail = state.detail
      const formData = new FormData()
      for (const entry of Object.entries(detail)) {
        if (entry[0] === 'photos') {
          for (const photo of entry[1]) {
            formData.append('photos[]', photo.file, photo.name())
          }
        } else {
          formData.append(entry[0], entry[1])
        }
      }
      await this.$repositories.act.update(contragentId, packageId, formData)
      this.$toast.success('Акт успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  },
  async [types.CREATE_ACT] ({ dispatch, state }, { contragentId, packageId }) {
    try {
      const detail = state.detail
      const formData = new FormData()
      for (const entry of Object.entries(detail)) {
        if (entry[0] === 'photos') {
          for (const photo of entry[1]) {
            formData.append('photos[]', photo.file, photo.name())
          }
        } else {
          formData.append(entry[0], entry[1])
        }
      }
      await this.$repositories.act.create(contragentId, packageId, formData)
      this.$toast.success('Акт успешно добавлен')
    } catch (error) {
      this.$toast.error(error.message)
    }
  }
}

export const getters = {}
