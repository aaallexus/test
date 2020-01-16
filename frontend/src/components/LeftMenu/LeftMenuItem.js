import React from 'react'


let LeftMenuItem=(props)=>
(
    <li className="active">
        <a href="./dashboard.html">
            <i className="nc-icon nc-bank"></i>
            <p>{props.item.title}</p>
        </a>
    </li>

)

export default LeftMenuItem
