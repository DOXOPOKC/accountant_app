import axios from 'axios'

const baseDomain = 'http://jud-module.lf.ru/'
const baseURL = `${baseDomain}`

export default axios.create({
  baseURL
})
