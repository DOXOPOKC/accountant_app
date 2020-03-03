// export default function ({ $axios, redirect, store }) {
//   $axios.onResponse(async response => {
//     if(response.status === 401) {
//       const originalRequest = response.config
//       originalRequest.baseURL = ''
//       originalRequest._retry = true
//       const newToken = await store.dispatch('refreshToken')
//       if(newToken) {
//         originalRequest.headers['Authorization'] = `Bearer ${newToken}`
//         return $axios(originalRequest)
//       } else {
//         redirect(301, '/account/login')
//       }
//     }
//     return response
//   })

//   $axios.onError(error => {
//     const code = parseInt(error.response && error.response.status)
//     if (code === 400) {
//       redirect('/400')
//     }
//   })
// }
