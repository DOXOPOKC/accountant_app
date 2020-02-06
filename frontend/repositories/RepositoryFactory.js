import ContragentRepository from './ContragentRepository'

const repositories = {
  contragents: ContragentRepository
}

export default {
  get: name => repositories[name]
}
