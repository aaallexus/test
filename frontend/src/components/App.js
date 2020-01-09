import React, {Component} from 'react'
import  Users from '../containers/Users'
import logo from './logo.svg';
import './App.css';

class App extends Component{
    render (){
        console.log(this.props)
        return (
            <div className="App">
                {this.props.children}
            </div>
        )
	}
}

export default App;
