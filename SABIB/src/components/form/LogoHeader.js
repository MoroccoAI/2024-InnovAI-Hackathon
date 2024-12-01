import React from 'react';
import logo from "../../assets/img/sabib.png";
import classes from "./css/LogoHeader.module.css";

function LogoHeader() {
  return (
    <div className={classes.logoBar}>
      <img className={classes.logo} src={logo} alt="" />
    </div>
  )
}

export default LogoHeader