import { useEffect } from 'react'
import {assets} from '../assets/assets'
import './ChatArea.css'
import { fetchQueryResponse } from '../services/api_calls'

function ChatArea() {
    useEffect(()=>{
        const fetchData = async()=>{
            console.log("fethcing query response")
            const data = await fetchQueryResponse({query:"who is an authorized person?"});
            console.log(data)
        }
        fetchData();
    },[]);
  return (
    <div className="chat-main-area">
        <div className="chat-nav">
            <p>Sherlock</p>
            <img src={assets.user_icon}></img>
        </div>
        <div className="chat-main-container">
            <div className="greet">
                <div className="name-greet">
                    <p><span >Hello, Erin.</span></p>
                </div>
                <div className="general-greet">
                    <p>How can I help you today?</p>
                </div>
            </div>
            <div className="cards">
                <div className="card">
                    <p>Give all IMAs with Force Majeure Clause</p>
                    <img src={assets.compass_icon}></img>
                </div>
                <div className="card">
                    <p>Who is an authorized person?</p>
                    <img src={assets.bulb_icon}></img>
                </div>
                <div className="card">
                    <p>Who do i need to contact in an emergency?</p>
                    <img src={assets.message_icon}></img>
                </div>
                <div className="card">
                    <p>Other queries you can suggest</p>
                    <img src={assets.code_icon}></img>
                </div>
            </div>
            <div className="chat-main-bottom">
                <div className="search-box">
                    <input type='text' placeholder='Enter the prompt here'/>
                    <div>
                        <img src={assets.gallery_icon}alt="" />
                        <img src={assets.mic_icon} alt="" />
                        <img src={assets.send_icon} alt="" />
                    </div>
                </div>
                <p className="bottom-info">
                    This is a product of GQG's Rapid Innovation Group (RIG). Please refer to the company's Generative AI policy for information on ethical and legal use of AI.
                </p>
            </div>
        </div>
    </div>
  )
}

export default ChatArea