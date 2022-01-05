import React from 'react'
import { Link } from 'react-router-dom'
export default function TestComponent(){
    return (<div>
                <label>Hello</label>
                <Link to='/users'>Next</Link>
            </div>)
}
