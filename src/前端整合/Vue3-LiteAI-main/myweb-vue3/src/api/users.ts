import request from '@/utils/request'

type LoginInfo = {
  username: string
  code?: string
  password: string
  base64str: string
}

type UserInfo = {
  username: string
  password: string
  identity: boolean
  base64str: string
}

type LoginResult = {
  success: boolean
  state: number
  message: string
  content: string
}

export const login = (loginInfo: LoginInfo) => {
  return request<LoginResult>({
    method: 'POST',
    url: '/users/login',
    data: `username=${loginInfo.username}&password=${loginInfo.password}`
  })
}

export const addUser = (userInfo: UserInfo) => {
  return request<LoginResult>({
    method: 'POST',
    url: '/users/addUser',
    data: `username=${userInfo.username}&password=${userInfo.password}&base64str=${userInfo.base64str}&identity=${userInfo.identity}`
  })
}

export const loginByFace = (loginInfo: LoginInfo) => {
  return request<LoginResult>({
    method: 'POST',
    url: '/users/loginByFace',
    data: `username=${loginInfo.username}&password=${loginInfo.password}&base64str=${loginInfo.base64str}`
  })
}

export const logout = () => {
  return request({
    method: 'POST',
    url: '/users/logout'
  })
}
