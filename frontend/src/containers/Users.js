import { connect } from 'react-redux'
import Users from '../components/Users'
import { inc, dec, loadHot } from '../actions'

const mapStateToProps = function(state)
{
    return ({
        users:state.users
    })
}
const mapDispatchToProps = (dispatch,ownProps) => ({
    onLoadHot: () => dispatch(loadHot())
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Users)

