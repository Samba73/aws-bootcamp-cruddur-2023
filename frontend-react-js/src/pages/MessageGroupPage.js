import React                from "react";
import { useParams }        from 'react-router-dom';
import {get}                from '../lib/Requests';
import {checkAuth}          from '../lib/CheckAuth';
import DesktopNavigation    from '../components/DesktopNavigation';
import MessageGroupFeed     from '../components/MessageGroupFeed';
import MessageFeed          from '../components/MessageFeed';
import MessageForm          from '../components/MessageForm';
import './MessageGroupPage.css';

export default function MessageGroupPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadMessageGroupsData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`
    get(url,{
      auth: true,
      success: function(data){
        setMessageGroups(data)
      }
    })
  }
  console.log('messagegrppage',messageGroups)
  const loadMessageGroupData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${params.message_group_uuid}`
    get(url,{
      auth: true,
      success: function(data){
        setMessages(data)
      }
    })
  }
  console.log('messagegrppage',messages)
  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadMessageGroupsData();
    loadMessageGroupData();
    checkAuth(setUser);
  }, [])
  return (
<article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
      {messageGroups && messageGroups.length > 0 && messageGroups.map((message_groups) => {
          return <MessageGroupFeed key={message_groups.message_group_uuid} message_groups={message_groups} />;
        })}
      </section>
      <div className='content messages'>
        <MessageFeed messages={messages} />
        <MessageForm setMessages={setMessages} />
      </div>
    </article>
  );
}
