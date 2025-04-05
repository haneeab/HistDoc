import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LogIn from "./LogIn";
import HomepageUser from "./HomepageUser";
import HomePage from "./HomePage";
import HomepageResearcher from "./HomepageResearcher";
import DeveloperModelsPage from "./DeveloperModelsPage"
import Register from "./Register";
import UserImages from "./UserImages";
import AboutUs from "./AboutUs";
import FeedbackPage from "./FeedbackPage"
import DeveloperModelFeedback from "./DeveloperModelFeedback"
import AllModelsFeedbackSummary from "./AllModelsFeedbackSummary"
import SortedModelsPage from "./SortedModelsPage"
function App() {
  return (
    <Router>
      <Switch>
        <Route path="/AllModelsFeedbackSummary" component={AllModelsFeedbackSummary} />
        <Route path="/LogIn" component={LogIn} />
        <Route path="/SortedModelsPage" component={SortedModelsPage} />

        <Route path="/feedback/:extraction_id" component={FeedbackPage} />
        <Route path="/about-us" component={AboutUs} />
        <Route path="/user-images" component={UserImages} />
        <Route path="/developer-feedbacks" component={DeveloperModelFeedback} />

        <Route path="/Register" component={Register} />
        <Route path="/homepage-user" component={HomepageUser} />
        <Route path="/developer-models" component={DeveloperModelsPage} />
        <Route path="/researcher-homepage" component={HomepageResearcher} />
        <Route exact path="/" component={HomePage} />
      </Switch>
    </Router>
  );
}

export default App;
import ReactDOM from "react-dom";

ReactDOM.render(<App />, document.getElementById("app"));