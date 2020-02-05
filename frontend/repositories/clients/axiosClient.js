import axios from 'axios'

const baseDomain = 'http://localhost'
const baseURL = `${baseDomain}` // Incase of /api/v1;

export default axios.create({
  baseURL,
  headers: {
    Authorization: `Token ${token}`
  }
})
