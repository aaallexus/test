import React from 'react'
import { act } from "react-dom/test-utils"
import configureStore from 'redux-mock-store'
import { Provider } from 'react-redux'

import { render, unmountComponentAtNode } from "react-dom"

import Users from '../containers/Users'
import TestComponent from '../components/TestComponent'

const initialState = { users:{caption:"Hello"} };
const mockStore = configureStore();
let store;

let container = null;
beforeEach(() => {
    store = mockStore(initialState);
	container = document.createElement("div");
	document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});


/*it("Render and Test dummy component", () => {
    act(()=>{
        render(<TestComponent/>, container)
    })
    expect(container.querySelector("label").textContent).toBe('Hello')
})*/
it("Render and Test Redux component", () => {
    act(()=>{
        render(<Provider store={store}><Users/></Provider>,container)
    })
//    expect(container.find(Users).length).toEqual(1);
    expect(container.querySelector("label").textContent).toBe('Hello')


    //expect(document.querySelector('[data-testid="button1"]')).toBeTruthy()
    store = mockStore({ users:{caption:"Hell"}});
    expect(container.querySelector("label").textContent).toBe('Hello')
})
