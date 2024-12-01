import React from "react";
import { Link } from "react-router-dom";
import LogoDark from "../../../assets/img/sabib.png"; // Import the SVG as a default import

const Logo = () => {
  return (
    <Link to="/">
      <img src={LogoDark} alt="Logo" style={{ width: "100px" }} /> {/* Render the SVG image using <img> */}
    </Link>
  );
};

export default Logo;
