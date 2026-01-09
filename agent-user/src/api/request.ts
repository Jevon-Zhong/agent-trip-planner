import type { ApiResponse, UserLoginResType, UserLoginType } from "@/types"

// 公共域名
const baseUrl = 'http://127.0.0.1:8000'

// 图片上传（头像）
export const uploadImageApi = (url: string) => {
    return new Promise((resolve, reject) => {
        uni.uploadFile({
            url: `${baseUrl}/user/upload_image`,
            filePath: url,
            name: 'file',
            success: (res) => {
                resolve(JSON.parse(res.data).data.upload_image_url)
            },
            fail: (err) => {
                reject(err)
            }
        })
    })
}

// 公用网络请求
const request = <T>(url: string, method: 'GET' | 'POST', data?: any): Promise<T> => {
    return new Promise((resolve, reject) => {
        uni.request({
            url: baseUrl + url,
            method,
            data,
            success: (res) => {
                const status = res.statusCode
                switch (status) {
                    case 200:
                        resolve(res.data as T)
                        break
                    case 404:
                        console.error('404')
                        reject('404')
                        break
                    case 401:
                        console.error('401')
                        reject('401')
                        uni.navigateTo({ url: '/pages/login/index' })
                        break
                    case 400:
                    case 422:
                        console.error(res.data)
                        reject('400 | 422')
                        uni.showToast({
                            title: '参数不对',
                            icon: 'none'
                        })
                        break
                    case 500:
                    case 501:
                    case 502:
                    case 503:
                        console.error('服务器发生错误')
                        reject('服务器发生错误')
                        uni.showToast({
                            title: '服务器发生错误',
                            icon: 'none'
                        })
                        break

                }
            },
            fail: (err) => {
                uni.showToast({
                    title: '出现异常',
                    icon: 'none'
                })
            }
        })
    })
}

// 登陆接口
export const userLoginApi = (params: UserLoginType):Promise<ApiResponse<UserLoginResType>> => {
    return request('/user/login', 'POST', params)
}
