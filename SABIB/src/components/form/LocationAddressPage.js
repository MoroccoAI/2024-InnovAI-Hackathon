import React, { useContext, useState, useEffect } from "react";
import classes from "./css/Form.module.css";
import FormContext from "../form/store/form-context";

function LocationAddressPage() {
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [region, setRegion] = useState("");
  const [postalCode, setPostalCode] = useState("");

  const { formData, setFormData, setCurrentPage, validation, setValidation } = useContext(FormContext);

  // useEffect to set initial field values when component mounts
  useEffect(() => {
    setAddress(formData.address || "");
    setCity(formData.city || "");
    setRegion(formData.region || "");
    setPostalCode(formData.postalCode || "");
  }, []);

  const handleAddressChange = (event) => {
    const value = event.target.value;
    setAddress(value);
    setFormData((prevData) => ({ ...prevData, address: value }));
    validateForm();
  };

  const handleCityChange = (event) => {
    const value = event.target.value;
    setCity(value);
    setFormData((prevData) => ({ ...prevData, city: value }));
    validateForm();
  };

  const handleRegionChange = (event) => {
    const value = event.target.value;
    setRegion(value);
    setFormData((prevData) => ({ ...prevData, region: value }));
    validateForm();
  };

  const handlePostalCodeChange = (event) => {
    const value = event.target.value;
    setPostalCode(value);
    setFormData((prevData) => ({ ...prevData, postalCode: value }));
    validateForm();
  };

  const validateForm = () => {
    // Validate each field and update validation state
    const isAddressValid = address.trim() !== "";
    const isCityValid = city.trim() !== "";
    const isRegionValid = region.trim() !== "";
    const isPostalCodeValid = postalCode.trim() !== "";

    setValidation({
      ...validation,
      address: isAddressValid,
      city: isCityValid,
      region: isRegionValid,
      postalCode: isPostalCodeValid,
    });
  };

  const handleNextClick = () => {
    // Check if all fields are valid
    if (validation.address && validation.city && validation.region && validation.postalCode) {
      // Proceed to the next page
      setCurrentPage(page => page + 1);
    } else {
      // Display an error message if any field is invalid
      alert("Please fill out all fields.");
    }
  };
  const handleBackClick = () => {
    setCurrentPage((page) => page - 1);
  };


  return (
    <div className={classes.container}>
      <span className={`${classes.container} ${classes.headings}`}>

        <h3>Add Location Address</h3>
      </span>
      <div className="mb-3">
        <label htmlFor="addressInput" className="form-label">
          Address
        </label>
        <input
          type="text"
          className={`form-control ${validation.address === false ? "is-invalid" : ""}`}
          id="addressInput"
          value={address}
          onChange={handleAddressChange}
        />
        {validation.address === false && <div className="invalid-feedback">Address should not be empty</div>}
      </div>
      <div className="mb-3">
        <label htmlFor="cityInput" className="form-label">
          City
        </label>
        <input
          type="text"
          className={`form-control ${validation.city === false ? "is-invalid" : ""}`}
          id="cityInput"
          value={city}
          onChange={handleCityChange}
        />
        {validation.city === false && <div className="invalid-feedback">City should not be empty</div>}
      </div>
      <div className="mb-3">
        <label htmlFor="regionInput" className="form-label">
          Region
        </label>
        <input
          list="morocco-regions"
          className={`form-control ${validation.region === false ? "is-invalid" : ""}`}
          name="region"
          value={region}
          onChange={handleRegionChange}
          placeholder="Type or select a region"
        />
        {validation.region === false && <div className="invalid-feedback">Region should not be empty</div>}
        <datalist id="morocco-regions">
          <option value="Rabat-Salé-Kénitra" />
          <option value="Casablanca-Settat" />
          <option value="Tanger-Tétouan-Al Hoceima" />
          <option value="Marrakech-Safi" />
          <option value="Fès-Meknès" />
          <option value="Oriental" />
          <option value="Souss-Massa" />
          <option value="Draa-Tafilalet" />
          <option value="Béni Mellal-Khénifra" />
          <option value="Guelmim-Oued Noun" />
          <option value="Laâyoune-Sakia El Hamra" />
          <option value="Dakhla-Oued Ed-Dahab" />
        </datalist>
      </div>
      <div className="mb-3">
        <label htmlFor="postalCodeInput" className="form-label">
          Postal Code
        </label>
        <input
          type="number"
          className={`form-control ${validation.postalCode === false ? "is-invalid" : ""}`}
          id="postalCodeInput"
          value={postalCode}
          onChange={handlePostalCodeChange}
        />
        {validation.postalCode === false && <div className="invalid-feedback">Postal Code should not be empty</div>}
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

export default LocationAddressPage;
