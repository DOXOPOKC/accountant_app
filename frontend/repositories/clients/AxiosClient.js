import axios from 'axios'

const protocol = process.env.NUXT_ENV_PROTOCOL
const domain = process.env.NUXT_ENV_DOMAIN

const baseDomain = 'http://jud-module.lf.ru'
const baseURL = `${baseDomain}`

export default axios.create({
  baseURL
})
