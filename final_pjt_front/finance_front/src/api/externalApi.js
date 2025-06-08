// src/api/externalApiFactory.js
import axios from 'axios'

export function createExternalApi({ baseURL, apiKey }) {
  const instance = axios.create({ baseURL, timeout: 10000 })

  instance.interceptors.request.use((config) => {
    console.group('[External API Request]', config.method.toUpperCase())
    console.log(config.baseURL + config.url, config.params || config.data)
    if (apiKey) config.headers['X-API-KEY'] = apiKey
    console.groupEnd()
    return config
  })

  instance.interceptors.response.use(
    (response) => {
      console.group('%c[External API Response]', 'font-weight:bold;color:#4CAF50;')
      console.log('Status:', response.status)
      console.log('URL:', response.config.baseURL + response.config.url)
      console.log('Response ▶')
      // console.log(response)
      console.log(response?.data?.response?.body)
      console.groupEnd()
      return response?.data?.response?.body
    },
    (error) => {
      console.group('%c[External API Response Error]', 'font-weight:bold;color:#F44336;')
      console.error('Status:', error.response?.status)
      console.error('URL:', error.response?.config?.url)
      console.error('Error ▶', error.response?.data || error)
      console.groupEnd()
      return Promise.reject(error)
    },
  )

  return instance
}
