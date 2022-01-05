import { connect } from 'react-redux'
import Navbar from '../components/Navbar'
import { logout } from '../actions/main'

const mapStateToProps = function(state)
{
    return {}
}
const mapDispatchToProps = function(dispatch,ownProps){
    return {
        logout: () => dispatch(logout())
    }
}
/*const mapDispatchToProps = (dispatch,ownProps) => ({
    logout: () => dispatch(logout())
})*/

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Navbar)

