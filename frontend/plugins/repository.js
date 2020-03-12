import createContragentRepository from '~/repositories/ContragentRepository'
import createPackageRepository from '~/repositories/PackageRepository'
import createTaskRepository from '~/repositories/TasksRepository'
import createNormRepository from '~/repositories/NormRepository'
import createSignUsers from '~/repositories/SignUsersRepository'
import createFiles from '~/repositories/FilesRepository'

export default (ctx, inject) => {
  const contragentRepository = createContragentRepository(ctx.$axios)
  const packageRepository = createPackageRepository(ctx.$axios)
  const taskRepository = createTaskRepository(ctx.$axios)
  const normRepository = createNormRepository(ctx.$axios)
  const signUserRepository = createSignUsers(ctx.$axios)
  const filesRepository = createFiles(ctx.$axios)

  const repositories = {
    contragents: contragentRepository('/contragents'),
    packages: packageRepository('/contragents'),
    tasks: taskRepository('/tasks'),
    norms: normRepository('/norms'),
    signUsers: signUserRepository('/sign_users'),
    files: filesRepository('/contragents')
  }

  inject('repositories', repositories)
}
