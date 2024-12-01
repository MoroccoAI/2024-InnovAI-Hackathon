import React, { useContext, useState, useEffect } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";
import InputSlider from "react-input-slider";

function FloorsAndBathroomsPage() {
  const { formData, setFormData, setCurrentPage } = useContext(FormContext);
  const [floors, setFloors] = useState(formData.floors || 1); // State variable for number of floors
  const [bathrooms, setBathrooms] = useState(formData.bathrooms || 1); // State variable for number of bathrooms

  // Function to handle changing the number of floors
  const handleFloorsChange = (value) => {
    setFloors(value);
  };

  // Function to handle changing the number of bathrooms
  const handleBathroomsChange = (value) => {
    setBathrooms(value);
  };

  // Function to handle navigation to the next page
  const handleNextClick = () => {
    // Update form data with selected number of floors and bathrooms
    setFormData((prevData) => ({
      ...prevData,
      floors: floors,
      bathrooms: bathrooms
    }));
    // Proceed to the next page
    setCurrentPage(page => page + 1);
  };

  const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };


  // Set the initial values of floors and bathrooms when the component mounts
  useEffect(() => {
    // Retrieve the floors and bathrooms values from formData and set them as the initial states
    setFloors(formData.floors || 1);
    setBathrooms(formData.bathrooms || 1);
  }, []);

  return (
    <div className={classes.container}>
      <span className={`${classes.container} ${classes.headings}`}>
        <h3>How many floors are there?</h3>
      </span>
      <div className="mb-4">
      <div style={{ marginBottom: "10px" }}>Floors: {floors}</div>
        <InputSlider
          axis="x"
          x={floors}
          xmin={1}
          xmax={10} // Assuming maximum 10 floors
          onChange={({ x }) => handleFloorsChange(x)}
          styles={{
            track: {
              backgroundColor: "#ddd",
              height: "10px",
            },
            active: {
              backgroundColor: "#0071be",
              height: "10px",
            },
            thumb: {
              width: "20px",
              height: "20px",
              marginTop: "-5px",
              backgroundColor: "#0071be",
            },
          }}
        />
      </div>

      <span className={`${classes.container} ${classes.headings}`}>
        <h3>How many bathrooms are there?</h3>
      </span>
      <div className="mb-4">
      <div style={{ marginBottom: "10px" }}>Bathrooms: {bathrooms}</div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <InputSlider
            axis="x"
            x={bathrooms}
            xmin={1}
            xmax={10} // Assuming maximum 5 bathrooms
            onChange={({ x }) => handleBathroomsChange(x)}
            styles={{
              track: {
                backgroundColor: "#ddd",
                height: "10px",
              },
              active: {
                backgroundColor: "#0071be",
                height: "10px",
              },
              thumb: {
                width: "20px",
                height: "20px",
                marginTop: "-5px",
                backgroundColor: "#0071be",
              },
            }}
          />
        </div>
      </div>

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

export default FloorsAndBathroomsPage;
