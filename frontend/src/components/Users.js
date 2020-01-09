import React,{Component} from 'react'
import { Link } from 'react-router-dom'
class Users extends Component{
//    <Link to='/'>Next</Link>
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
