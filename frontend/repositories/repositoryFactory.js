import contragentRepository from './contragentRepository'

const repositories = {
  posts: contragentRepository
}

export default {
  get: name => repositories[name]
}
