export function loginRequest(param) {
    return {
        type: 'LOGIN',
        payload: {
            request: {
                url:'/token/',
                method:'POST',
                data:{
                    username:param.login,
                    password:param.password
                },
            },
        },
    }
}
export function logout(){
    return {
        type: 'LOGOUT'
    }
}
export const setAccessToken = (accessToken) =>{
    return{
        type:'SET_ACCESS_TOKEN',
        'accessToken':accessToken
    }

}
