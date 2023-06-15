import MessageGroupItem     from './MessageGroupItem';
import MessageGroupNewItem  from './MessageGroupNewItem';
import FormErrors           from '../components/FormErrors';
import React, { useState }  from 'react';
import './MessageGroupFeed.css';
import { post } from '../lib/Requests';

export default function MessageGroupFeed(props) {
  console.log('final props', props)
  const data = props.message_groups['data']
  console.log('data', data)
  const { message_groups } = data;
  const [showModal, setShowModal] = useState(false);
  const [message, setMessage] = useState('');
  const [handle, setHandle] = useState('');
  const [errors, setErrors] = React.useState([]);


    const handleNewMessage = () => {
      setShowModal(true);
      //setHandle(props.message_groups.handle)
    };

    const handleCancel = () => {
      setShowModal(false);
      setMessage('');
    };

    const handleSubmit = async (event) => {
      event.preventDefault();
      const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages`
      const payload_data = {
        message: message,
        handle: handle
      }
      post(url, payload_data, {
        auth: true,
        setErrors: setErrors,
        success: function(data){
          props.setMessage(current => [data,...current]);
          setMessage('')
          setShowModal(false);
        }
      })
    } 

    const handleInputChange = (event) => {
      setMessage(event.target.value);
    };
    const handleChange = (event) => {
      setHandle(event.target.value);
    };
    
  let message_group_new_item;
  if (props.otherUser) {
    message_group_new_item = <MessageGroupNewItem user={props.otherUser} />
  }
  //console.log('messagegroupfeed', props)
  //console.log('issue', props.message_groups.data)
  //let message_groups = props.message_groups.data || []; // Initialize with an empty array if props.message_groups is undefined

  return (
    <div className='message_group_feed'>
      <div className='message_group_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div className="right-aligned-button">
        <button type="button" className="black-button" onClick={handleNewMessage}>
          New Message
        </button>
        {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>New Message</h2>
            <input value={handle} onChange={handleChange} />
            <textarea value={message} onChange={handleInputChange} />
            <div className="modal-buttons">
              <button type="button" onClick={handleCancel}>
                Cancel
              </button>
              <button type="button" onClick={handleSubmit}>
                Submit
              </button>
            </div>
          </div>
          <FormErrors errors={errors} />
        </div>
      )}
      </div>
      <div className="message_group_feed_collection">
        {message_group_new_item}
        {Array.isArray(message_groups) && message_groups.length > 0 ? (
          message_groups.map((message_group) => (
            <MessageGroupItem
              key={message_group.uuid}
              message_group={message_group}
            />
          ))
        ) : (
          <p>No message groups found.</p>
        )}
      </div>
    </div>
  );
}
