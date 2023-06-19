import { Link }                               from "react-router-dom";
import MessageFeed                            from './MessageFeed';
import { format_datetime, message_time_ago }  from '../lib/DateTimeFormats';
import { useParams }                          from 'react-router-dom';
import './MessageGroupItem.css';

export default function MessageGroupItem(props) {
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
      {message_group.length > 0 && message_group.map(([key, value]) => (
          <MessageFeed key={key} messages={value} />
        ))}
      </div>
    </Link>
  );
}