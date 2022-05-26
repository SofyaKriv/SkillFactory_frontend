import React, {useState} from "react";
import PropTypes, {object} from "prop-types";
import { Link } from "react-router-dom";
import axios from "axios";

//import "./VideoShow.css";


function VideoShow(props) {
    const [userId, setUserId] = useState('');
    if (!userId.length) {
        axios.get(`http://localhost:8000/api/users/`).then(res => {
            for (let d in res.data) {
                if (res.data[d].username === props.video.author) {
                    setUserId(res.data[d].id);
                }
            }
        });
    }
    return (
        <React.Fragment>
        <tr>
            <tr><h3>{ props.video.title }</h3></tr>
            <tr>
                <video className="center" width="800" controls>
                    <source src={ props.video.video }  type='video/mp4'/>
                </video>
            </tr>
            <tr>
                Автор: <Link to={`/chat/22/${ userId }`} >{ props.video.author }</Link>
            </tr>
        </tr>
        </React.Fragment>
    )
}


export default VideoShow;



