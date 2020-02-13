import ContragentRepository from '~/repositories/ContragentRepository'
import PackageRepository from '~/repositories/PackageRepository'
import TasksRepository from '~/repositories/TasksRepository'
import NormRepository from '~/repositories/NormRepository'

const repositories = {
  contragents: ContragentRepository,
  packages: PackageRepository,
  tasks: TasksRepository,
  norms: NormRepository
}

export default {
  get: name => repositories[name]
}
