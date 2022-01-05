import React from 'react'
import { createHashHistory,createBrowserHistory/*, createMemoryHistory*/} from 'history'
import { render, unmountComponentAtNode } from "react-dom"



export default function renderWithRouter(
    ui,
    {
        route = '/',
        history = createBrowserHistory({ initialEntries: [route] }),
    } = {}
)
{
    const Wrapper = ({ children }) => (
        <Provider store={store}><ConnectedRouter history={history}><App>{children}</App></ConnectedRouter></Provider>
    )
    return {
        ...render(ui, Wrapper),
        // adding `history` to the returned utilities to allow us
       // to reference it in our tests (just try to avoid using
       // this to test implementation details).
       history,
    }
} 
