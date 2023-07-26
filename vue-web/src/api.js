// vue-web\src\api.js

// 请求拦截器
// // 请求拦截器
// axios.interceptors.request.use(config => {
//   const accessToken = localStorage.getItem('access_token')
//   const refreshToken = localStorage.getItem('refresh_token')
  
//   // 如果access_token为空,使用refresh_token获取新的access_token
//   if (!accessToken) { 
//     return axios.post('/refresh_token', { refresh_token: refreshToken })
//       .then(res => {
//         // 获取新的access_token和refresh_token并保存
//         localStorage.setItem('access_token', res.data.access_token)
//         localStorage.setItem('refresh_token', res.data.refresh_token)
        
//         // 使用新的access_token重新发起请求
//         config.headers.Authorization = `Bearer ${res.data.access_token}` 
//         return config  
//       })
//   }
  
//   // 如果access_token未过期,直接使用
//   config.headers.Authorization = `Bearer ${accessToken}`  
//   return config
// })

// // 响应拦截器
// axios.interceptors.response.use(res => res, err => {
//   // 如果返回401,调用刷新token接口获取新的access_token
//   if (err.response.status === 401) {
//     const refreshToken = localStorage.getItem('refresh_token')
//     return axios.post('/refresh_token', { refreshToken })
//       .then(res => {
//         const accessToken = res.data.access_token
//         localStorage.setItem('access_token', accessToken)
        
//         // 使用新的access_token重新发起请求
//         err.config.headers.Authorization = `Bearer ${accessToken}` 
//         return axios(err.config) 
//       })
//   }
// })
// export const login = (data) => axios.post(`${API_URL}/login`, data)
// export const getProfile = () => axios.get(`${API_URL}/profile`)
// export const logout = () => axios.post(`${API_URL}/logout`)
// export const updateProfile = (data) => axios.put(`${API_URL}/profile/update`, data)

// 登录  
// export const login = (data) => {  
//   return axios.post(`${API_URL}/login`, data)
//     .then(res => {
//       localStorage.setItem('access_token', res.data.access_token)
//       console.log('Login succeeded.',res.data.access_token)
//     }) 
// }
// 登录接口

// vue-web\src\api.js
import axios from 'axios'
import jwt_decode from 'jwt-decode'
const API_URL = 'http://localhost:5000'
// axios配置
axios.defaults.baseURL = API_URL
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.delete['Content-Type'] = 'application/json'
axios.defaults.headers.get['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`

export const login = (data) => {
  return new Promise((resolve, reject) => {
    axios.post('/login', data)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
}
// 获取用户信息
export const getProfile = () => {
  return new Promise((resolve, reject) => {
    axios.get('/profile', {   // 增加配置对象,设置请求头
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })  
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
}
 

// 更新用户信息
export const updateProfile = (user) => {
  return new Promise((resolve, reject) => {
    axios.put('/profile/update', user, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`  
      }
    })
    .then(res => {
      resolve(res)
    })
    .catch(err => {
      reject(err) 
    })
  })
}

export const logout = () => {
  return new Promise((resolve, reject) => {
    const access_token = localStorage.getItem('access_token')
    if (!access_token) {
      reject(new Error('No access_token found.'))
    }
    axios.post('/logout', {}, {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    })
    .then(res => {
      resolve(res) 
      localStorage.removeItem('access_token')
    })
    .catch(err => {
      reject(err)
    })
  })
}

export const register = (data) => { 
  // 使用用户名、密码和身份证号进行注册
  console.log('调用注册接口,参数:', data)
  return new Promise((resolve, reject) => {
    axios.post('/users/register', data)  
    .then(res => {  
      // 注册成功,返回结果  
      console.log('注册成功:', res.data)
      resolve(res)
    })
    .catch(err => {
      // 注册失败,返回错误 
      console.log('注册失败:', err.response.data)  
      reject(err)
    })
  })
} 



export const generateUnpaidBill = (data) => {
  // 获取本地存储的用户角色
  // 解码 access_token,获取 claims
  const accessToken = localStorage.getItem('access_token')
  const claims = jwt_decode(accessToken, 'secret')
  console.log('claims:', claims)
  const role = claims.privilege
  console.log('调用生成未付账单接口, 参数:', data,role)
  // 方法主体结构
  return new Promise((resolve, reject) => {
    // 权限判断
    if (role !== 0) {        
      return reject('权限不足,无法生成未付账单')
    }
    
    axios.post('/bills/generate', data, {
      headers: {
        Authorization: `Bearer ${accessToken}`  
      }
    })
    .then(res => {
      console.log('生成未付账单成功, 结果:', res.data)  
      resolve(res)
    }).catch(err => {
      console.log('生成未付账单失败, 错误:', err.response.data)    
      reject(err)
    })
  })   
}

export const queryUnpaidBills = () => {
  
  return new Promise((resolve, reject) => {
   
    axios.get('/bills', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`  
      }
    }).then(res => {
    console.log('查询未付账单成功, 结果:', res.data);
    resolve(res)
  }).catch(err => {
    console.log('查询未付账单失败, 错误:', err);
    reject(err)
  });
})
}

export const makePayment = (data) => {
  
  console.log('调用付款接口, 参数:', data);
  return new Promise((resolve, reject) => {
    axios.post('/payments', data, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`  
      }
    }).then(res => {
    console.log('付款成功, 结果:', res.data);
    resolve(res)
  }).catch(err => {
    console.log('付款失败, 错误:', err);
    reject(err)
  });
})
}

export const getClerkUnpaidBills = () => {
  // 获取本地存储的用户角色
  const accessToken = localStorage.getItem('access_token')
  const claims = jwt_decode(accessToken, 'secret')
  console.log('claims:', claims)
  const role = claims.privilege

  console.log('调用获取职员未付账单接口', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`  
    }

  });
  return new Promise((resolve, reject) => {
     // 权限判断
     if (role !== 1) {  
      return reject('权限不足,无法生成未付账单')
    }
    axios.get('/clerk/unpaid_bills').then(res => {
    console.log('获取职员未付账单成功,结果:', res);
    resolve(res)
  }).catch(err => {
    console.log('获取职员未付账单失败, 错误:', err.data);
    reject(err)
  });
})
}

export const clerkCharge = (data) => {
  // 获取本地存储的用户角色
  const accessToken = localStorage.getItem('access_token')
  const claims = jwt_decode(accessToken, 'secret')
  console.log('claims:', claims)
  const role = claims.privilege
  console.log('调用职员收费接口, 参数:', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`  
    }
  });
  return new Promise((resolve, reject) => {
    if (role !== 1) {  
      return reject('权限不足,无法生成未付账单')
    }
    axios.post('/clerk/charge', data).then(res => {
    console.log('职员收费成功, 结果:', res.data);
    resolve(res)
  }).catch(err => {
    console.log('职员收费失败, 错误:', err.data);
    reject(err)
  });
})
}
export const hardDelete = (data) => {
  // 获取本地存储的用户角色
  const accessToken = localStorage.getItem('access_token')
  const claims = jwt_decode(accessToken, 'secret')
  console.log('claims:', claims)
  // const role = claims.privilege
  console.log('调用删除接口, 参数:', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`  
    }
  });
  return new Promise((resolve, reject) => {
    // if (role !== 1) {  
    //   return reject('权限不足,无法删除用户')
    // }
    axios.delete('/users/hard_delete', data).then(res => {
    console.log('删除成功, 结果:', res.data);
    resolve(res)
  }).catch(err => {
    console.log('删除失败, 错误:', err.data);
    reject(err)
  });
})
}
export const softDelete = (data) => {
  // 获取本地存储的用户角色
  const accessToken = localStorage.getItem('access_token')
  const claims = jwt_decode(accessToken, 'secret')
  console.log('claims:', claims)
  // const role = claims.privilege
  console.log('调用删除接口, 参数:', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`  
    }
  });
  return new Promise((resolve, reject) => {
    // if (role !== 1) {  
    //   return reject('权限不足,无法删除用户')
    // }
    axios.post('/users/soft_delete', data).then(res => {
    console.log('删除成功, 结果:', res.data);
    resolve(res)
  }).catch(err => {
    console.log('删除失败, 错误:', err.data);
    reject(err)
  });
})
}

// export const register = (data) => axios.post(`${API_URL}/users/register`, data)
export default axios