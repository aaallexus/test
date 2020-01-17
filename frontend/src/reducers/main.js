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
            console.log(action.payload);
            if(action.payload.status===200 && action.payload.statusText==='OK')
            {
                return {
                    ...state,
                    isAuth:true,
                    accessToken:action.payload.data.access,
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
        default :
            return state
    }
}

