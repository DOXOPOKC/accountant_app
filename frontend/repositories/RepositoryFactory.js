import ContragentRepository from '~/repositories/ContragentRepository'
import PackageRepository from '~/repositories/PackageRepository'
import TasksRepository from '~/repositories/TasksRepository'

const repositories = {
  contragents: ContragentRepository,
  packages: PackageRepository,
  tasks: TasksRepository
}

export default {
  get: name => repositories[name]
}
