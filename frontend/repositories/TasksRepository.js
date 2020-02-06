import client from '~/repositories/clients/AxiosClient'

const resource = '/api/tasks'

export default {
  // Возвращает список пакетов с документами конкретного контрагента
  get (taskId) {
    return client.get(`${resource}/${taskId}`)
  }
}
