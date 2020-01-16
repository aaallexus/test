export function loginRequest(param) {
    return {
        type: 'LOGIN',
        payload: {
            request: {
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
