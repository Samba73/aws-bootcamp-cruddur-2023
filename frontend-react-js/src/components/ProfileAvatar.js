import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
  console.log('profile avatar', props)
  const backgroundImage = props.id!= null ? `url("https://assets.cruddur.in/avatars/${props.id}.jpg")` : "none";
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div 
      className="profile-avatar"
      style={styles}
    ></div>
  );
}
