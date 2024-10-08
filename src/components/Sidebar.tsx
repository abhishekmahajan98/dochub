import './Sidebar.css'
import {assets} from '../assets/assets'
import { useState } from 'react'
const Sidebar = () => {
    const [extended,setExtended] = useState(true)
  return (
    <div className='sidebar'>
        <div className="top">
            <img className='menu' src={assets.menu_icon} alt="menu icon" onClick={()=>setExtended(!extended)}></img>
            <div className="new-chat">
                <img src={assets.plus_icon}></img>
                {extended?<p>New Chat</p>:null}
            </div>
            {extended?
            <div className="recent">
                <p className="recent-title">Recent</p>
                <div className="recent-entry">
                    <img src={assets.message_icon}></img>
                    <p>Give me all IMAs...</p>
                </div>
            </div>
            :null}
        </div>
        <div className="bottom">
            <div className="bottom-item recent-entry">
                <img src={assets.question_icon}></img>
                {extended?<p>Help</p>:null}
            </div>
            <div className="bottom-item recent-entry">
                <img src={assets.history_icon}></img>
                {extended?<p>Activity</p>:null}
            </div>
            <div className="bottom-item recent-entry">
                <img src={assets.setting_icon}></img>
                {extended?<p>Settings</p>:null}
            </div>
        </div>
    </div>
  )
}

export default Sidebar