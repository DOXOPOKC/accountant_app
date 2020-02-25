import Repository from '~/repositories/RepositoryFactory'

// const contragentRepository = Repository.get('contragents')
const TasksRepository = Repository.get('tasks')

export const types = {
  SET_TASK: 'SET_TASK',
  REMOVE_TASK_: 'REMOVE_TASK_UID',

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
  async [types.FETCH_TASKS] ({ state, commit, getters }) {
    try {
      const tasksStatus = getters.tasksStatus()
      while (tasksStatus) {
        const { data } = (await Promise.all([
          await new Promise(resolve => setTimeout(() => resolve(), 2000)),
          await TasksRepository.get(state.taskUid)
        ]))[1]
        console.log(data, 1488)
        if (!data.length) {
          console.log(data, 1337)
          commit(types.REMOVE_TASK_UID)
        }
        commit(types.SET_TASKS, data)
      }
    } catch (error) {
      console.error(error)
    }
    // const failedTasks = tasksGroup.filter(task => task.success === false)
  }
}

export const getters = {
  tasksStatus: state => !!state.taskUid
}
