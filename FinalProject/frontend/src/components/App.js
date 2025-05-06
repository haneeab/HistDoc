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
import AnnotateModelEditor from "./AnnotateModelEditor"
import FeedbackPage from "./FeedbackPage"
import DeveloperModelFeedback from "./DeveloperModelFeedback"
import AllModelsFeedbackSummary from "./AllModelsFeedbackSummary"
import SortedModelsPage from "./SortedModelsPage"
import ManuscriptListPage from "./ManuscriptListPage"
import ManuscriptFilesPage from "./ManuscriptFilesPage"
import GroundFoldersPage from "./GroundFoldersPage"
import GroundXMLFilesPage from "./GroundXMLFilesPage"
import XMLAnnotatorPage  from "./XMLAnnotatorPage"
import ModelSelectionPage from "./ModelSelectionPage"
import DeveloperModelParameters from "./DeveloperModelParameters"
import DeveloperTestModelPage from "./DeveloperTestModelPage"
function App() {
  return (
    <Router>
      <Switch>
        <Route path="/AllModelsFeedbackSummary" component={AllModelsFeedbackSummary} />
        <Route path="/LogIn" component={LogIn} />
        <Route path="/SortedModelsPage" component={SortedModelsPage} />
        <Route exact path="/ManuscriptListPage" component={ManuscriptListPage} />

        <Route path="/feedback/:modelId" component={FeedbackPage} />
        <Route path="/about-us" component={AboutUs} />
        <Route path="/user-images" component={UserImages} />
        <Route path="/developer-feedbacks" component={DeveloperModelFeedback} />
        <Route path="/ManuscriptFilesPage" component={ManuscriptFilesPage} />
        <Route path="/select-model" component={ModelSelectionPage} />
<Route path="/annotate-model/:modelId" component={AnnotateModelEditor} />
        <Route path="/developer-test-model" component={DeveloperTestModelPage} />

        <Route path="/Register" component={Register} />
        <Route path="/homepage-user" component={HomepageUser} />
        <Route path="/developer-models" component={DeveloperModelsPage} />
        <Route path="/researcher-homepage" component={HomepageResearcher} />
        <Route exact path="/GroundFoldersPage" component={GroundFoldersPage} />
                        <Route exact path="/" component={HomePage} />
                <Route exact path="/XMLAnnotatorPage" component={XMLAnnotatorPage} />
<Route exact path="/developer-model-parameters/:id" component={DeveloperModelParameters} />

                <Route exact path="/GroundXMLFilesPage" component={GroundXMLFilesPage} />
      </Switch>
    </Router>
  );
}//
// ManuscriptFilesPage
export default App;
import ReactDOM from "react-dom";

ReactDOM.render(<App />, document.getElementById("app"));