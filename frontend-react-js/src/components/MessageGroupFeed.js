import './MessageGroupFeed.css';
import MessageGroupItem from './MessageGroupItem';
import MessageGroupNewItem from './MessageGroupNewItem';
import React, { useState } from 'react';

export default function MessageGroupFeed(props) {
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState('');
    const [handle, setHandle] = useState('');
    //const [newmessage, setNewMessage] = useState([]);
  
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
      try {
        const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages`
        console.log('onsubmit payload', message)
        console.log('handle is', handle)
        let json = {
          'message': message,
          'handle': handle
        }
        const res = await fetch(backend_url, {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(json),
        });
      
        //let data = await res.json();
        if (res.status === 200) {
          //props.setMessages('Test')
          //props.setNewMessage(current => [...current,data]);
          console.log('message saved')
        } else {
          console.log(res)
        }
      } catch (err) {
        console.log(err);
      }
    };
  
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

  return (
    
      <div className='message_group_feed'>
      <div className='message_group_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div>
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
        </div>
      )}
      </div>
      <div className='message_group_feed_collection'>
        {message_group_new_item}
        {props.message_groups.map(message_group => {
          return  <MessageGroupItem key={message_group.message_group_uuid} message_group={message_group} />
      })}
      </div>
    </div>


    </div>
   
  );
}