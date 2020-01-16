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

const history = createBrowserHistory()
//const history = createHashHistory()
//const history = createMemoryHistory()

const client = axios.create({
//	baseURL: 'http://catalogue.nlu.org.ua/new/rest/api.php',
    baseURL: 'http://192.168.1.26/cxbi/rest.php',
	responseType: 'json',
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

console.log(history);

let store = createStore(
  createRootReducer(history),
  composeEnhancers(applyMiddleware(axiosMiddleware(client))),
);

/*const store = createStore(
    createRootReducer(history),
    composeWithDevTools(
        applyMiddleware(
          routerMiddleware(history),      
          thunkMiddleware
        )
    )
)
*/

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
