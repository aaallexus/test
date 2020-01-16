import { connect } from 'react-redux'
import LoginForm from '../components/LoginForm'
import { loginRequest } from '../actions/main'

const mapStateToProps = function(state)
{
    return ({
        auth:state.auth
    })
}
const mapDispatchToProps = (dispatch,ownProps) => ({
    onLoginRequest: (param) => dispatch(loginRequest(param))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginForm)

