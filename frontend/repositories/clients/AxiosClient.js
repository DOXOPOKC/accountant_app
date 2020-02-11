import axios from 'axios'

const baseDomain = 'http://localhost/'
const baseURL = `${baseDomain}`

export default axios.create({
  baseURL
})
