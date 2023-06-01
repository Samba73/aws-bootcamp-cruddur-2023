import './DesktopSidebar.css';
import Search from '../components/Search';
import TrendingSection from '../components/TrendingsSection'
import SuggestedUsersSection from '../components/SuggestedUsersSection'
import JoinSection from '../components/JoinSection'
import { Routes, Route, Link } from "react-router-dom";

export default function DesktopSidebar(props) {
  const trendings = [
    {"hashtag": "100DaysOfCloud", "count": 2053 },
    {"hashtag": "CloudProject", "count": 8253 },
    {"hashtag": "AWS", "count": 9053 },
    {"hashtag": "FreeWillyReboot", "count": 7753 }
  ]

  function About() {
    return <h2>About Cruddur</h2>
  }
  function TermsofService() {
    return <h2>Terms of Service</h2>
  }
  function PrivacyPolicy() {
    return <h2>Privacy Policy</h2>
  }
  const users = [
    {"display_name": "vishnu r", "handle": "vishnu"}
  ]

  let trending;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
  }

  let suggested;
  if (props.user) {
    suggested = <SuggestedUsersSection users={users} />
  }
  let join;
  if (props.user) {
  } else {
    join = <JoinSection />
  }

  return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <Link to="/about">About</Link>
        <Link to="/tos">Terms of Service</Link>
        <Link to="/pp">Privacy Policy</Link>
      </footer>
      <Routes>
        <Route path="/about">
          <About />
        </Route>
        <Route path="/to">
          <TermsofService />
        </Route>
        <Route path="/pp">
          <PrivacyPolicy />
        </Route>
      </Routes>
    </section>
  );
}
