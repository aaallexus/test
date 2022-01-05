import { connect } from 'react-redux'
import Users from '../components/Users'
import { getUsersList } from '../actions/users'

const mapStateToProps = function(state, ownProps)
{
    return ({
        users:state.users
    })
}
const mapDispatchToProps = (dispatch,ownProps) => ({
   getUsersList: () => dispatch(getUsersList())
})
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Users)

