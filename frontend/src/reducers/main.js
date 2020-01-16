var initialState={
    sessionId:0,
    menu:[
        {   
                                        title:'Users'
                                    },
                                {   
                                                                title:'Settings'
                                                            }
    ],
    isAuth:false
}
export default function (state = initialState, action) {
    switch(action.type){
        case 'LOGIN':
            return {
                ...state,
            }
        case 'LOGIN_SUCCESS':
            if(action.payload.data.result=='ok')
            {
                return {
                    ...state,
                    isAuth:true,
                    sessionId:2,
                    menu:[
                        {
                            title:'Users'
                        },
                        {
                            title:'Settings'
                        }
                    ]
                }
            }
            else
                return state
        case 'LOGOUT':
            return {
                ...state,
                isAuth:false,
                sessionId:0
            }
        default :
            return state
    }
}

