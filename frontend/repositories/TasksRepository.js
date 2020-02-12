import client from '~/repositories/clients/AxiosClient'

const resource = '/api/tasks'

export default {
  get (taskId) {
    return client.get(`${resource}/${taskId}/`)
  }
}
