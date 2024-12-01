import React, { useContext, useState, useEffect } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";

function LocationSizePage() {
  const [size, setSize] = useState(""); // State variable for selected size
  const { formData, setFormData, setCurrentPage } = useContext(FormContext);

  // Function to handle size selection
  const handleSizeSelect = (selectedSize) => {
    setSize(selectedSize);
  };

  const handleNextClick = () => {
    // Check if size is selected
    if (size) {
      // Update form data with selected size
      setFormData((prevData) => ({ ...prevData, size: size }));
      // Proceed to the next page
      setCurrentPage(page => page + 1);
    } else {
      // Display an error message if size is not selected
      alert("Please select a size to proceed.");
    }
  };
  const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };



  // Set the initial value of size when the component mounts
  useEffect(() => {
    // Retrieve the size value from formData and set it as the initial state
    setSize(formData.size || "");
  }, []);

  return (
    <div className={classes.container}>
      <span className={`${classes.container} ${classes.headings}`}>
        <h3>How big is this location?</h3>
      </span>
      <div className="btn-group-vertical">
        <div className="mb-2 mt-4">
          <input
            type="radio"
            id="lessThan60"
            name="size"
            value="Less than 60 m2"
            checked={size === "Less than 60 m2"}
            onChange={() => handleSizeSelect("Less than 60 m2")}
            className="visually-hidden"
          />
          <label
            htmlFor="lessThan60"
            className={`btn btn-outline-primary ${size === "Less than 60 m2" ? "active" : ""} ${classes.customButton}`}
            style={{ cursor: "pointer" }}
          >
            Less than 60 m2
          </label>
        </div>

    <div className="mb-2 mt-4">
          <input
            type="radio"
            id="60to80"
            name="size"
            value="60 - 80 m2"
            checked={size === "60 - 80 m2"}
            onChange={() => handleSizeSelect("60 - 80 m2")}
            className="visually-hidden"
          />
          <label
            htmlFor="60to80"
            className={`btn btn-outline-primary ${size === "60 - 80 m2" ? "active" : ""}`}
            style={{ cursor: "pointer" }}
          >
            60 - 80 m2
          </label>
        </div>
        <div className="mb-2 mt-4">
          <input
            type="radio"
            id="80to120"
            name="size"
            value="80 - 120 m2"
            checked={size === "80 - 120 m2"}
            onChange={() => handleSizeSelect("80 - 120 m2")}
            className="visually-hidden"
          />
          <label
            htmlFor="80to120"
            className={`btn btn-outline-primary ${size === "80 - 120 m2" ? "active" : ""}`}
            style={{ cursor: "pointer" }}
          >
            80 - 120 m2
          </label>
        </div>
        <div className="mb-2 mt-4">
          <input
            type="radio"
            id="moreThan120"
            name="size"
            value="More than 120 m2"
            checked={size === "More than 120 m2"}
            onChange={() => handleSizeSelect("More than 120 m2")}
            className="visually-hidden"
          />
          <label
            htmlFor="moreThan120"
            className={`btn btn-outline-primary ${size === "More than 120 m2" ? "active" : ""}`}
            style={{ cursor: "pointer" }}
          >
            More than 120 m2
          </label>
        </div>      </div>
        <div className={classes.navigationButtons}>
        <button className={`button-back ${classes.customButton}`} onClick={handleBackClick}>
          Back
        </button>
        <button className={`button  ${classes.customButton}`} onClick={handleNextClick}>
          Next
        </button>
      </div>
    </div>
  );
}

export default LocationSizePage;
