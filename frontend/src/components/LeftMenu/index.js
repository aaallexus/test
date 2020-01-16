import React,{Component} from 'react'
import PropTypes from 'prop-types'
import LeftMenuItem from './LeftMenuItem.js'


class LeftMenu extends Component{
    render(){
        return (<div class="sidebar-wrapper">
            <ul class="nav">
            {this.props.menu.map(menuItem=>
                <LeftMenuItem item={menuItem}/>
             )
            }
            </ul>    
        </div>)
    }
}

LeftMenu.propTypes = {
    menu:PropTypes.array,
}

export default LeftMenu
