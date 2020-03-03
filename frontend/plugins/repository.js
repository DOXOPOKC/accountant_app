import createContragentRepository from '~/repositories/ContragentRepository'
import createPackageRepository from '~/repositories/PackageRepository'
import createTaskRepository from '~/repositories/TasksRepository'
import createNormRepository from '~/repositories/NormRepository'
import createSignUsers from '~/repositories/SignUsersRepository'

export default (ctx, inject) => {
  // inject the repository in the context (ctx.app.$repository)
  // And in the Vue instances (this.$repository in your components)
  const contragentRepository = createContragentRepository(ctx.$axios)
  const packageRepository = createPackageRepository(ctx.$axios)
  const taskRepository = createTaskRepository(ctx.$axios)
  const normRepository = createNormRepository(ctx.$axios)
  const signUserRepository = createSignUsers(ctx.$axios)

  const repositories = {
    contragents: contragentRepository('/contragents'),
    packages: packageRepository('/contragents'),
    tasks: taskRepository('/contragents'),
    norms: normRepository('/contragents'),
    signUsers: signUserRepository('/contragents')
  }

  inject('repositories', repositories)
}
