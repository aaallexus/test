import { combineReducers } from 'redux'
import { connectRouter } from 'connected-react-router'
import main from './main'
import users from './users'


export default (history) => combineReducers({
    router: connectRouter(history),
    main,
    users,
})



