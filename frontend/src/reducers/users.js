var initialState={
        userList:[],
        isRequest:false,
        caption:"Hello"
}
export default function users(state = initialState, action) {
    switch(action.type){
        case 'LOAD_HOT':
            return {
                ...state,
            }
        case 'LOAD_HOT_SUCCESS':
            return {
                ...state,
                caption:action.payload.data.title
            }
        default :
            return state
    }
}
