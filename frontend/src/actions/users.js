export function getUsersList() {
    return {
        type: 'GET_USERS_LIST',
        payload: {
            request: {
				url:'/v1/users/all/',
                method:'GET',
                data:{
                },
            },
        },
    }
}

