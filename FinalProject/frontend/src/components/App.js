import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";
import Register from "./Register";
import LogIn from "./LogIn";
import Navbar from "./Navbar";
import HomepageUser from "./HomepageUser";
import UserImages from "./UserImages";
import AboutUs from "./AboutUs";
export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <HomePage />
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);