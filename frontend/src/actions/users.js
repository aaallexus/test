export function getUsersList() {
    return {
        type: 'GET_USERS_LIST',
        payload: {
            request: {
				url:'/v1/users/all/',
                method:'POST',
                headers:{
                    'Authorization':"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5NTEzMjE3LCJqdGkiOiIyMmJiOWIxNmVkOTk0NTFkYjQ4ZjEwNWRiNTU2NTFiMyIsInVzZXJfaWQiOjF9.EGZrrcl4z-hCOTvVwIDh50V9LVW63i8DXncQM2GMmkk"
                },
                data:{
                },
            },
        },
    }
}

