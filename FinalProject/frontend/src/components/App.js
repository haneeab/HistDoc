import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LogIn from "./LogIn";
import HomepageUser from "./HomepageUser";
import HomePage from "./HomePage";
import HomepageResearcher from "./HomepageResearcher";
import Register from "./Register";

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/LogIn" component={LogIn} />                {/* ✅ Fixed */}
        <Route path="/Register" component={Register} />
        <Route path="/homepage-user" component={HomepageUser} />
        <Route path="/researcher-homepage" component={HomepageResearcher} />
        <Route exact path="/" component={HomePage} />
      </Switch>
    </Router>
  );
}

export default App;
import ReactDOM from "react-dom";  // ✅ THIS IS MISSING in your error

ReactDOM.render(<App />, document.getElementById("app"));  // ✅ Make sure your HTML has <div id="app"></div>
