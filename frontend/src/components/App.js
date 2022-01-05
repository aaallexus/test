import React, {Component} from 'react'
import LoginForm from '../containers/LoginForm'
import Navbar from '../containers/Navbar'
import LeftMenu from '../containers/LeftMenu'
class App extends Component{
    render (){
        const {main} = this.props
        return (
            <>
            {!main.isAuth ? (
                <LoginForm/>
            ) : (
            <div className="wrapper ">
                <div className="sidebar" data-color="white" data-active-color="danger">
                    <LeftMenu/>
                </div>
                <div className="main-panel">
                    <Navbar/>
                    <div className="content">
                        {this.props.children}
                    </div>
                </div>
            </div>
            )
            }
            </>
        )
	}
}

export default App;
