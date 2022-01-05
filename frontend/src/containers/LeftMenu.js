import { connect } from 'react-redux'
import LeftMenu from '../components/LeftMenu/index.js'
import { loadHot } from '../actions'

const mapStateToProps = function(state, ownProps)
{
    return ({
        menu:state.main.menu
    })
}
const mapDispatchToProps = (dispatch,ownProps) => ({
})

export default connect(
      mapStateToProps,
      mapDispatchToProps
)(LeftMenu)

