import React from 'react'
import {Link} from 'react-router-dom'


let LeftMenuItem=(props)=>
(
    <li className="active">
        <Link to={props.item.url} activeClassName="active">
            <i className="nc-icon nc-bank"></i>
            <p>{props.item.title}</p>
        </Link>
    </li>

)

export default LeftMenuItem
