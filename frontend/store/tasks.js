export const types = {
  SET_TASK: 'SET_TASK',

  REMOVE_TASK_UID: 'REMOVE_TASK_UID',

  SET_TASKS: 'SET_TASKS',
  REMOVE_TASKS: 'REMOVE_TASKS',
  FETCH_TASKS: 'FETCH_TASKS'
}

export const state = () => ({
  taskUid: '1337',
  tasks: null
})

export const mutations = {
  [types.SET_TASK] (state, payload) {
    state.taskUid = payload
  },
  [types.SET_TASKS] (state, payload) {
    state.tasks = payload
  },
  [types.REMOVE_TASKS] (state, payload) {
    state.tasks.splice(state.tasks.indexOf(payload), 1)
  },
  [types.REMOVE_TASK_UID] (state) {
    state.taskUid = ''
  }
}

export const actions = {
  async [types.FETCH_TASKS] ({ state, commit, getters }, { contragentId, packageId, taskUid }) {
    try {
      while (getters.tasksStatus) {
        const responses = (await Promise.all([
          await new Promise(resolve => setTimeout(() => resolve(), 1000)),
          await this.$repositories.tasks.get(taskUid),
          await this.$repositories.packages.getPackage(contragentId, packageId)
        ]))
        const tasks = responses[1]
        const contragentPackage = responses[2]
        if (!tasks.length) { commit(types.REMOVE_TASK_UID) }
        commit(types.SET_TASKS, tasks)
        this.commit('packages/SET_PACKAGE', contragentPackage)
        // this.dispatch('packages/FETCH_PACKAGE', { contragentId, packageId })
      }
    } catch (error) {
      this.$toast.error('Ошибка!')
    }
    // const failedTasks = tasksGroup.filter(task => task.success === false)
  }
}

export const getters = {
  tasksStatus: state => !!state.taskUid
}
