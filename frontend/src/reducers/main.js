var initialState={
    menu:[
        {   
            title:'Users',
            url:'/users/',
        },
        {   
            title:'Settings',
            url:'/setting/',
        }
    ],
    isAuth:false,
    accessToken:null,
    refreshToken:null
}
export default function (state = initialState, action) {
    switch(action.type){
        case 'LOGIN':
            return {
                ...state,
            }
        case 'LOGIN_SUCCESS':
            if(action.payload.status===200 && action.payload.statusText==='OK')
            {
                let tokenParts=action.payload.data.access.split('.');
                return {
                    ...state,
                    isAuth:true,
                    accessToken:action.payload.data.access,
                    accessTokenExpire:JSON.parse(atob(tokenParts[1])).exp*1000,
                    refreshToken:action.payload.data.refresh,
/*                    menu:[
                        {
                            title:'Users'
                        },
                        {
                            title:'Settings'
                        }
                    ]*/
                }
            }
            else
                return state
        case 'LOGOUT':
            return {
                ...state,
                isAuth:false,
                accessToken:null,
                refreshToken:null
            }
        case 'SET_ACCESS_TOKEN':
            return {
                ...state,
                accessToken:action.accessToken
            }
        default :
            return state
    }
}

