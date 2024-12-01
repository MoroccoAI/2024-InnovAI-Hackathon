import React, { useContext } from "react";
import classes from "./css/Form.module.css";
import { HomeIcon, OfficeBuildingIcon } from "@heroicons/react/solid";
import FormContext from "./store/form-context";

function TypeOfLocation() {
  const types = [
    {
      id: "1",
      icon: <HomeIcon className={classes.icon} />,
      title: "Single-family",
    },
    {
      id: "2",
      icon: <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={classes.icon}>
        <path d="M19.006 3.705a.75.75 0 1 0-.512-1.41L6 6.838V3a.75.75 0 0 0-.75-.75h-1.5A.75.75 0 0 0 3 3v4.93l-1.006.365a.75.75 0 0 0 .512 1.41l16.5-6Z" />
        <path fillRule="evenodd" d="M3.019 11.114 18 5.667v3.421l4.006 1.457a.75.75 0 1 1-.512 1.41l-.494-.18v8.475h.75a.75.75 0 0 1 0 1.5H2.25a.75.75 0 0 1 0-1.5H3v-9.129l.019-.007ZM18 20.25v-9.566l1.5.546v9.02H18Zm-9-6a.75.75 0 0 0-.75.75v4.5c0 .414.336.75.75.75h3a.75.75 0 0 0 .75-.75V15a.75.75 0 0 0-.75-.75H9Z" clipRule="evenodd" />
      </svg>,
      title: "Villa",
    },
    {
      id: "3",
      icon: <OfficeBuildingIcon className={classes.icon} />,
      title: "Apartment",
    },
    {
      id: "4",
      icon: <HomeIcon className={classes.icon} />,
      title: "Other",
    },
  ];

  const { formData, setFormData, setCurrentPage } = useContext(FormContext);

  const insertType = (id) => {
    setFormData((prevData) => ({ ...prevData, type: id }));
  };

  const handleNextClick = () => {
    // Validate fields specific to this page, if necessary
    // For example, check if a type is selected
    if (!formData.type) {
      // Display an error message or prevent navigation
      alert("Please select a type of location.");
      return; // Stop navigation
    }

    // Navigate to the next page
    setCurrentPage((prevPage) => prevPage + 1);
  };

  return (
    <>
      <span className={`${classes.container} ${classes.headings}`}>
        <h3>What type of location is this?</h3>
      </span>

      <div className={classes.container_row}>
        {types.map((item) => (
          <div
            key={item.id}
            className={`${classes.useCard} ${formData.type === item.id ? classes.active : ""
              }`}
            onClick={() => insertType(item.id)}
          >
            {item.icon}
            <h4 className={classes.title}>{item.title}</h4>
          </div>
        ))}
      </div>

      <button className="button" onClick={handleNextClick}>
        Next
      </button>
    </>
  );
}

export default TypeOfLocation;
