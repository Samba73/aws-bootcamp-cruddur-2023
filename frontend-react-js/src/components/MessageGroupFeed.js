import './MessageGroupFeed.css';
import MessageGroupItem from './MessageGroupItem';
import MessageGroupNewItem from './MessageGroupNewItem';
export default function MessageGroupFeed(props) {
  let message_group_new_item;
  if (props.otherUser) {
    message_group_new_item = <MessageGroupNewItem user={props.otherUser} />
  }
  console.log('messagegroupfeed', props)
  console.log('issue', props.message_groups.data)
  let message_groups = props.message_groups.data || []; // Initialize with an empty array if props.message_groups is undefined

  return (
    <div className='message_group_feed'>
      <div className='message_group_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div className='message_group_feed_collection'>
        {message_group_new_item}
        {message_groups.map(message_group => {
        return  <MessageGroupItem key={message_group.message_group_uuid} message_group={message_group} />
        })}
      </div>
    </div>
  );
}