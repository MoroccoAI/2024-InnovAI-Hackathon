import React, { useContext, useState, useEffect } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";

function NicknamePage() {
  const [nickname, setNickname] = useState(""); 
  const { formData, setFormData, validation, setValidation, setCurrentPage } = useContext(FormContext);

  useEffect(() => {
    // Set initial value of the nickname field when the component mounts
    setNickname(formData.nickname || "");
  }, []);

  const handleNicknameChange = (event) => {
    const value = event.target.value;
    setNickname(value);
    // Validate nickname field and update validation state
    if (value.trim() !== "") {
      setValidation((prevValidation) => ({ ...prevValidation, nickname: true }));
    } else {
      setValidation((prevValidation) => ({ ...prevValidation, nickname: false }));
    }
  };

  const handleNextClick = () => {
    // Move to the next page if nickname is not empty
    if (validation.nickname) {
      setFormData((prevData) => ({ ...prevData, nickname: nickname }));
      setCurrentPage(page => page + 1);
    } else {
      alert("Please provide a nickname to proceed.");
    }
  };
  const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };


  return (
    <div className={classes.container}>
            <span className={`${classes.container} ${classes.headings}`}>

      <h3>Give a location nickname</h3>
</span>
      <div className="mb-3">
        <label htmlFor="nicknameInput" className="form-label">
          Nickname
        </label>
        <input
          type="text"
          className={`form-control ${validation.nickname === false ? "is-invalid" : ""}`}
          id="nicknameInput"
          value={nickname}
          onChange={handleNicknameChange}
        />
        {validation.nickname === false && <div className="invalid-feedback">Nickname should not be empty</div>}
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

export default NicknamePage;
