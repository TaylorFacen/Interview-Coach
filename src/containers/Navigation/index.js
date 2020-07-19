import React from 'react';
import { Navbar } from 'react-bootstrap';

import './Navigation.css'

export default () => {
    return (
        <Navbar bg = "white" className = "Navigation">
            <Navbar.Brand href="/">Interview Coach</Navbar.Brand>
        </Navbar>
    )
}