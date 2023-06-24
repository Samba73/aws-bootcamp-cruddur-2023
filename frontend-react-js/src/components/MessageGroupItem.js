import React                                  from "react";
import { Link }                               from "react-router-dom";
import {get}                                  from '../lib/Requests';
import {checkAuth}                            from '../lib/CheckAuth';
import MessageFeed                            from './MessageFeed';
import { format_datetime, message_time_ago }  from '../lib/DateTimeFormats';
import { useParams }                          from 'react-router-dom';
import './MessageGroupItem.css';

export default function MessageGroupItem(props) {
  const [messages, setMessages] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();
  console.log('messagegroupitemprops', props)
  console.log('what i see here...',props.message_group.message_group_uuid)
  const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid === props.message_group.message_group_uuid){
      console.log('true', props.message_group)
      classes.push('active')
    }
    return classes.join(' ');
  }
  const message_group = Object.entries(props)

  const loadMessageGroupData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${props.message_group.message_group_uuid}`

    get(url,{
      auth: true,
      success: function(data){
        setMessages(data)
      }
    })
  }
  //console.log('groupitemurl',url)
  console.log('messagegroupitem setmessages', messages)
  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadMessageGroupData();
    checkAuth(setUser);
  }, [])
  console.log('messagegroupitem', message_group)
  return (
    <Link className={classes()} to={`/messages/`+props.message_group.message_group_uuid}>
      <div className='message_group_avatar'></div>
      <div className='message_content'>
        <div className='message_group_meta'>
          <div className='message_group_identity'>
            <div className='display_name'>{props.message_group.user_display_name}</div>
            <div className="handle">@{props.message_group.user_handle}</div>
          </div>{/* activity_identity */}
        </div>{/* message_meta */}
        <div className="message">{props.message_group.message}</div>
        <div className="created_at" title={format_datetime(props.message_group.created_at)}>
          <span className='ago'>{message_time_ago(props.message_group.created_at)}</span> 
        </div>{/* created_at */}
      </div>{/* message_content */}
      <div className='message_re-feed_collection'>
        {props.message_group && props.message_group.length > 0 && props.message_group.map(messages => {
        return  <MessageFeed messages={messages} />
        })}
      </div>
    </Link>
  );
}