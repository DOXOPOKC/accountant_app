import Repository from '~/repositories/RepositoryFactory'

// const contragentRepository = Repository.get('contragents')
const TasksRepository = Repository.get('tasks')

export const types = {
  SET_TASK: 'SET_TASK',
  REMOVE_TASK: 'REMOVE_TASK',

  FETCH_TASKS: 'FETCH_TASKS'
}

export const state = () => ({
  taskUid: ''
})

export const mutations = {
  [types.SET_TASK] (state, payload) {
    state.taskUid = payload
  },
  [types.REMOVE_TASK] (state, payload) {
    state.tasks.splice(state.tasks.indexOf(payload), 1)
  }
}

export const actions = {
  async [types.FETCH_TASKS] (state) {
    const taskUid = state.state.taskUid
    const { data: tasksGroup } = await TasksRepository.get(taskUid)
    const failedTasks = tasksGroup.filter(task => task.success === false)
    if (failedTasks) {}
  }
}

export const getters = {}
