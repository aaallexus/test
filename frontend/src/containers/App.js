import { connect } from 'react-redux'
import App from '../components/App'

const mapStateToProps = function(state)
{
    return ({
        main:state.main
    })
}
const mapDispatchToProps = (dispatch,ownProps) => ({
    dispatch
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

