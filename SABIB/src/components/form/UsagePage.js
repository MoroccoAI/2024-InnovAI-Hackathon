import React, { useContext } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";

function UsagePage() {
  const usageOptions = [
    { id: "primary", label: "Primary Residence" },
    { id: "vacation", label: "Vacation Home" },
    { id: "rent", label: "I rent it out" },
    { id: "other", label: "Other" },
  ];

  const { formData, setFormData, setCurrentPage, validation, setValidation } = useContext(FormContext);

  const handleOptionSelect = (optionId) => {
    setFormData((prevData) => ({ ...prevData, usage: optionId }));
    setValidation((prevData) => ({ ...prevData, usage: true }));
  };

  const handleNextClick = () => {
    // Move to the next page if the selection is valid
    if (validation.usage) {
      setCurrentPage((page) => page + 1);
    } else {
      alert("Please select an option to proceed.");
    }
  };

   const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };

  return (
    <div className={classes.container}>
      <span className={`${classes.container} ${classes.headings}`}>
        <h3>How do you use this location?</h3>
      </span>

      {usageOptions.map((option) => (
        <div key={option.id} className="mb-2 mt-4">
          <input
            type="radio"
            id={option.id}
            name="usage"
            value={option.id}
            checked={formData.usage === option.id}
            onChange={() => handleOptionSelect(option.id)}
            className="visually-hidden"
          />
          <label
            htmlFor={option.id}
            className={`btn btn-outline-primary ${formData.usage === option.id ? "active" : ""} ${classes.customButton}`}
            style={{ cursor: "pointer" }}
          >
            {option.label}
          </label>
        </div>
      ))}
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

export default UsagePage;
