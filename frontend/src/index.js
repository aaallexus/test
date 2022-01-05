import React from 'react'
import ReactDOM, {render} from 'react-dom'
import {Route} from 'react-router'
import { createStore, applyMiddleware,compose} from 'redux'
import { Provider } from 'react-redux'
import { ConnectedRouter } from 'connected-react-router'
import { createHashHistory,createBrowserHistory/*, createMemoryHistory*/} from 'history'

import axios from 'axios'


import axiosMiddleware from 'redux-axios-middleware'

import createRootReducer from './reducers'
import  Users from './containers/Users'

import './assets/css/index.css'
import './assets/css/style.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import App from './containers/App'
import TestComponent from './components/TestComponent'
import * as serviceWorker from './serviceWorker'
import {setAccessToken} from './actions/main.js'

const history = createBrowserHistory()
//const history = createHashHistory()
//const history = createMemoryHistory()

const client = axios.create({
    baseURL:'/api',
	esponseType: 'json',
    headers: {
        'Accept': '*/*',
        'Content-type': 'application/json'
    },
});
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

console.log(history);

const checkToken = store => next => action => {
    console.log('dispatching', action)
    console.log(store)
    client.defaults.headers.common['Authorization'] = 'Bearer  '+store.getState().main.accessToken
    if(action.type!=='LOGIN' 
        && action.type!=='SET_ACCESS_TOKEN'
        && action.type!='@@router/LOCATION_CHANGE')
    {
        if(store.getState().main.accessToken!==null)
        {
            let tokenExpire;
            try{
                let parts=store.getState().main.accessToken.split('.')
                tokenExpire=new Date(JSON.parse(atob(parts[1])).exp*1000)
            }
            catch{
            }
            let curTime=new Date();
            curTime.setMinutes(curTime.getMinutes()+4)
            console.log(tokenExpire,curTime)
            if(tokenExpire<=curTime)
            {
                client.post('/token/refresh/',{
                    refresh:store.getState().main.refreshToken
                })
                .then(function(response){
                    console.log(response.data.access);
                    store.dispatch(setAccessToken(response.data.access))
                    client.defaults.headers.common['Authorization'] = 'Bearer  '+response.data.access; 
                    return next(action)
                })

            }
            else
                return next(action)
        }
    }
    else
        return next(action)
}

let store = createStore(
  createRootReducer(history),
  composeEnhancers(applyMiddleware(checkToken,axiosMiddleware(client))),
);


render(
    <Provider store={store}>
        <ConnectedRouter  history={history}>
            <App>
                <Route exact path="/" component={TestComponent}/>
                <Route exact path="/users" component={Users}/>
            </App>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root')
)
    
//    render(<App />, document.getElementById('root'))

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
