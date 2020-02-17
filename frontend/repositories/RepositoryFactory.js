import ContragentRepository from '~/repositories/ContragentRepository'
import PackageRepository from '~/repositories/PackageRepository'
import TasksRepository from '~/repositories/TasksRepository'
import NormRepository from '~/repositories/NormRepository'
import SignUsers from '~/repositories/SignUsersRepository'

const repositories = {
  contragents: ContragentRepository,
  packages: PackageRepository,
  tasks: TasksRepository,
  norms: NormRepository,
  signUsers: SignUsers
}

export default {
  get: name => repositories[name]
}
