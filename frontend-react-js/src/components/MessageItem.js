import './MessageItem.css';
import { Link } from "react-router-dom";
import { format_datetime, message_time_ago, time_ago } from '../lib/DateTimeFormats';


  return (
    <Link className='message_item' to={`/messages/@`+props.message.user_handle}>
      <div className='message_avatar'></div>
      <div className='message_content'>
        <div className='message_meta'>
          <div className='message_identity'>
            <div className='display_name'>{props.message.user_display_name}</div>
            <div className="handle">@{props.message.user_handle}</div>
          </div>{/* activity_identity */}
        </div>{/* message_meta */}
        <div className="message">{props.message.message}</div>
        <div className="created_at" title={format_datetime(props.message.created_at)}>
          <span className='ago'>{message_time_go(props.message.created_at)}</span> 
        </div>{/* created_at */}
      </div>{/* message_content */}
    </Link>
  );
}
