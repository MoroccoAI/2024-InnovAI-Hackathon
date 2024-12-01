  import React, { useContext, useState, useEffect } from "react";
  import classes from "./css/Form.module.css";
  import FormContext from "../form/store/form-context";


  function PeopleCountPage() {
    const { formData, setFormData, setCurrentPage } = useContext(FormContext);
    const [peopleCount, setPeopleCount] = useState(formData.peopleCount || 1);

    const handleIncrement = () => {
      setPeopleCount((prevCount) => prevCount + 1);
    };

    const handleDecrement = () => {
      if (peopleCount > 1) {
        setPeopleCount((prevCount) => prevCount - 1);
      }
    };

    const handleNextClick = () => {
      // Update form data with selected people count
      setFormData((prevData) => ({ ...prevData, peopleCount: peopleCount }));
      // Proceed to the next page
      setCurrentPage(page => page + 1);
    };
    const handleBackClick = () => {
      setCurrentPage((page) => page - 1);
    };
  
    // Set the initial value of peopleCount when the component mounts
    useEffect(() => {
      // Retrieve the peopleCount value from formData and set it as the initial state
      setPeopleCount(formData.peopleCount || 1);
    }, []);

    return (
      <div className={classes.container}>
        <h3 className={classes.heading}>How many people live in this location?</h3>

        <div className={classes.section}>
          <button className={classes.controlButton} onClick={handleDecrement}>
            <i className="bi bi-dash"></i>
          </button>
          <span>{peopleCount}</span>
          <button className={classes.controlButton} onClick={handleIncrement}>
            <i className="bi bi-plus"></i>
          </button>
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

  export default PeopleCountPage;
