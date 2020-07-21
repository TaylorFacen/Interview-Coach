import React from 'react';
import { Image, Row, Col } from 'react-bootstrap';
import { RiQuestionAnswerLine } from 'react-icons/ri'
import { FaRegThumbsUp } from 'react-icons/fa'
import { AiOutlineMail } from 'react-icons/ai'

import heroImage from '../../images/hero-image.png'
import logo from '../../images/interview-coach-logo.png'
import './Home.css';

export default () => (
    <div className = "Home">
        <Row className = "hero">
            <Col sm = { 12 } md = { 7 } className = "hero-text">
                <div>
                    <h1>Prep for an interview on your own time</h1>
                    <p>
                        After answering a few questions, you'll get feedback that you can use to make each practice session better than the last!
                        <br></br>To get started, just text "Practice" to (617) 812-6224
                    </p>
                </div>
            </Col>
            <Col sm = { 12 } md = { 5 } className = "hero-image">
                <Image 
                    src = { heroImage } 
                    alt = "Hero image" 
                    fluid
                />
            </Col> 
        </Row>
        <Row className = "logo-section">
            <Image src = { logo } alt = "App logo" />
        </Row>
        <Row className = "app-details">
            <Col sm = { 12 } md = { 4 } lg = { 4 } className = "app-detail">
                <h5>Tailored Questions</h5>
                <div className = "details-icon">
                    <RiQuestionAnswerLine />
                </div>
                <p>Select questions based on the type of interview (e.g. behavioral, personal, school, etc.)</p>
            </Col>
            <Col sm = { 12 } md = { 4 } lg = { 4 } className = "app-detail">
                <h5>Instant Feedback</h5>
                <div className = "details-icon">
                    <FaRegThumbsUp />
                </div>
                <p>Receive feedback on important metrics like talking speed and number of filler words.</p>
            </Col>
            <Col sm = { 12 } md = { 4 } lg = { 4 } className = "app-detail">
                <h5>E-Mail Summary</h5>
                <div className = "details-icon">
                    <AiOutlineMail />
                </div>
                <p>Get a list of your questions and responses directly to your inbox. </p>
            </Col>
        </Row>
    </div>

)