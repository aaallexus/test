import React,{Component} from 'react'
class Users extends Component{
    componentDidMount(){
        this.props.getUsersList()
    }
    render(){
		var {users}=this.props
        return (<>
            <label>{users.caption}</label>
			<button onClick={this.props.onLoadHot}>SendAjax</button>
            <button data-testid="button2">asd</button>
        </>)
    }

}

export default Users
