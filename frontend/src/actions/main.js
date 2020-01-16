export function loginRequest(param) {
    return {
        type: 'LOGIN',
        payload: {
            request: {
                method:'POST',
                data:{
                    login:param.login,
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
