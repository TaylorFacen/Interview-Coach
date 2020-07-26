import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

import logo from '../../images/interview-coach-logo.png'
import './Navigation.css'

export default () => {
    return (
        <Navbar bg = "white" className = "Navigation">
            <Navbar.Brand href="/">
                <img 
                    src = { logo }
                    alt = "InterviewCoach logo"
                    width = "50"
                    height = "50"
                />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                <Nav.Link target="_blank" href = "https://www.buymeacoffee.com/interviewcoach">Support InterviewCoach</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}