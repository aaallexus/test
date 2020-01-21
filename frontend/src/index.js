import React from 'react'
import ReactDOM, {render} from 'react-dom'
import {Route} from 'react-router'
import { createStore, applyMiddleware,compose} from 'redux'
import { Provider } from 'react-redux'
import { ConnectedRouter } from 'connected-react-router'
import { createHashHistory,createBrowserHistory/*, createMemoryHistory*/} from 'history'

import axios from 'axios'


import {
      isLoggedIn,
      setAuthTokens,
      clearAuthTokens,
      getAccessToken,
      getRefreshToken
} from "axios-jwt"

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
//   baseURL: 'http://192.168.1.26/api/token/',
    baseURL: 'http://devci.naviwfm.com/api',
	responseType: 'json',
    headers: {
        'Accept': '*/*',
        'Content-type': 'application/json'
//        'Authorization':"asdasd",
    },
});
//client.defaults.headers.common['Authorization'] = 'asdasdasd';
setAuthTokens({
    accessToken:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5NTE2NTM4LCJqdGkiOiIwYWM5YjBjODBhMjI0MjJkYjBiZjZiM2QwMDQ1MGRiMyIsInVzZXJfaWQiOjF9.Bl4siepr3U6ETpJo8s7k36BZsueZpTCeRY7ceKvLA8g',
    refreshToken:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3OTYwMjYzOCwianRpIjoiZDg2NmZiMGQ1ZGI2NGY5YjhjMzA3ZTkwYjhmMjNkZmEiLCJ1c2VyX2lkIjoxfQ.C0O8Td2xsWMjeXDtOkqREDgse-O2BQc0P6rMgSoc9lw',
})
/*client.options('http://devci.naviwfm.com/api/token/',{
    responseType: 'json',
    headers: {
        'Accept': 'application/x-www-form-urlencoded',

    },
})*/
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

console.log(history);

const checkToken = store => next => action => {
    console.log('dispatching', action)
    console.log(store)
    if(action.type!=='LOGIN')
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
            console.log(tokenExpire,curTime)
            if(tokenExpire>=curTime)
            {
                client.post('/token/refresh/',{
                    refresh:store.getState().main.refreshToken
                })
                .then(function(response){
                    console.log(response.data.access);
//                    store.dispatch(setAccessToken(response.data.access))
                     client.defaults.headers.common['Authorization'] = 'Bearer  '+response.data.access; 
//                     return next(setAccessToken(response.data.access))
                    return next(action)
                })

            }
//          return next(action)
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
