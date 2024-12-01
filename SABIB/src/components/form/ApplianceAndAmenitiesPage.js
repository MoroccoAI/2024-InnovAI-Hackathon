import React, { useContext, useState, useEffect } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";
import Checkbox from '@mui/material/Checkbox';


function ApplianceAndAmenitiesPage() {
  const { formData, setFormData, setCurrentPage } = useContext(FormContext);
  const [selectedIndoorOptions, setSelectedIndoorOptions] = useState([]);
  const [selectedOutdoorOptions, setSelectedOutdoorOptions] = useState([]);

  // Define indoor and outdoor options
  const indoors = [
    "Bathtub",
    "Dishwasher",
    "Hot Tub",
    "Refrigerator with Ice Maker",
    "Washer/Dryer",
  ];

  const outdoors = [
    "Swimming Pool",
    "Swimming Pool with Auto Pool Filter",
    "Hot Tub",
    "Fountain",
    "Pond",
  ];

  // Function to handle selecting indoor options
  const handleIndoorOptionSelect = (option) => {
    const updatedIndoorOptions = selectedIndoorOptions.includes(option)
      ? selectedIndoorOptions.filter((item) => item !== option)
      : [...selectedIndoorOptions, option];
    setSelectedIndoorOptions(updatedIndoorOptions);
  };

  // Function to handle selecting outdoor options
  const handleOutdoorOptionSelect = (option) => {
    const updatedOutdoorOptions = selectedOutdoorOptions.includes(option)
      ? selectedOutdoorOptions.filter((item) => item !== option)
      : [...selectedOutdoorOptions, option];
    setSelectedOutdoorOptions(updatedOutdoorOptions);
  };

  // Set the initial values of selected options when the component mounts
  useEffect(() => {
    // Retrieve the selected indoor and outdoor options from formData and set them as the initial states
    setSelectedIndoorOptions(formData.selectedIndoorOptions || []);
    setSelectedOutdoorOptions(formData.selectedOutdoorOptions || []);
  }, []);

  // Function to handle navigating to the next page
  const handleNextClick = () => {
    // Update formData with the selected options
    setFormData((prevData) => ({
      ...prevData,
      selectedIndoorOptions,
      selectedOutdoorOptions,
    }));

    // Move to the next page
    setCurrentPage((prevPage) => prevPage + 1);
  };
  const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };

  return (
    <div className={classes.container}>
      <h3 className={classes.heading}>Appliance and Amenities</h3>
      <div className={classes.optionsContainer}>
        <div className={classes.optionCategory}>
          <h4 className={classes.subHeading}>Indoors:</h4>
          {indoors.map((option) => (
            <div key={option} className={classes.checkboxOption}>
              <Checkbox
                checked={selectedIndoorOptions.includes(option)}
                onChange={() => handleIndoorOptionSelect(option)}
                color="primary"
                inputProps={{ 'aria-label': 'controlled' }}
              />
              <label htmlFor={option} className={classes.checkboxLabel}>
                {option}
              </label>
            </div>
          ))}
        </div>

        <div className={classes.optionCategory}>
          <h4 className={classes.subHeading}>Outdoors:</h4>
          {outdoors.map((option) => (
            <div key={option} className={classes.checkboxOption}>
              <Checkbox
                checked={selectedOutdoorOptions.includes(option)}
                onChange={() => handleOutdoorOptionSelect(option)}
                color="primary"
                inputProps={{ 'aria-label': 'controlled' }}
              />
              <label htmlFor={option} className={classes.checkboxLabel}>
                {option}
              </label>
            </div>
          ))}
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

export default ApplianceAndAmenitiesPage;
