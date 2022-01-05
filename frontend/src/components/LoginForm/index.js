import React, {Component} from 'react'
import './css/main.css'
import './css/util.css'
import './fonts/font-awesome-4.7.0/css/font-awesome.min.css'

class LoginForm extends Component{
    constructor(props) {
		super(props);
		this.state = {login:'',password: ''};
        this.inputLogin = this.inputLogin.bind(this)
        this.inputPassword = this.inputPassword.bind(this)
        this.onSubmit=this.onSubmit.bind(this)
	}
    inputLogin(e){  
        this.setState({login:e.target.value})
    }
    inputPassword(e){
        this.setState({password:e.target.value})
    }
    onSubmit(e){
        this.props.onLoginRequest({
            login:this.state.login,
            password:this.state.password
        })
        e.preventDefault()
    }
    render(){
        return (
            <>
                <div className="limiter">
					<div className="container-login100">
						<div className="wrap-login100 p-l-85 p-r-85 p-t-55 p-b-55">
							<form className="login100-form validate-form flex-sb flex-w" onSubmit={this.onSubmit}>
								<span className="login100-form-title p-b-32">
                                    Login Form
								</span>

								<span className="txt1 p-b-11">
									Username
								</span>
								<div className="wrap-input100 validate-input m-b-36" data-validate = "Username is required">
									<input className="input100" type="text" name="username" value={this.state.login} onChange={this.inputLogin}/>
									<span className="focus-input100"></span>
								</div>
								
								<span className="txt1 p-b-11">
									Password
								</span>
								<div className="wrap-input100 validate-input m-b-12" data-validate = "Password is required">
									<input className="input100" type="password" value={this.state.password} onChange={this.inputPassword} />
									<span className="focus-input100"></span>
								</div>
								<div className="container-login100-form-btn">
									<button className="login100-form-btn">
										Login
									</button>
								</div>

							</form>
						</div>
					</div>
				</div>
            </>
        )
    }
}

export default LoginForm
