import React, { useState } from "react";
import { Link } from "react-router-dom";
import '../../form/css/global.css';

import {
  Navbar,
  Collapse,
  Nav,
  NavItem,
  NavbarBrand,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Dropdown,
  Button,
  Modal,
  ModalHeader,
  ModalBody,
} from "reactstrap";
import Logo from "../../../assets/img/sabib.png";
import { UserButton } from "@clerk/clerk-react";
import LandingFormPage from "../../form/LandingFormPage";
import FormProvider from "../../form/FromProvider";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);
  const toggleModal = () => setModalOpen(!modalOpen);

  return (
    <Navbar color="info" dark expand="md">
      <NavbarBrand href="/" className="d-lg-none">
        <img src={Logo} alt="Logo" style={{ width: "40px" }} />
      </NavbarBrand>
      <Button color="info" className="d-lg-none" onClick={toggle}>
        {isOpen ? <i className="bi bi-x"></i> : <i className="bi bi-three-dots-vertical"></i>}
      </Button>
      <Collapse navbar isOpen={isOpen}>
        <Nav className="me-auto" navbar>
          <NavItem>
            <Link to="starter" className="nav-link">
              Dashboard
            </Link>
          </NavItem>
          <NavItem>
            <Link to="/" className="nav-link">
              Home
            </Link>
          </NavItem>
          <UncontrolledDropdown inNavbar nav>
            <DropdownToggle caret nav>
              Menu
            </DropdownToggle>
            <DropdownMenu end>
              <DropdownItem onClick={toggleModal}>Add House</DropdownItem>
              <DropdownItem>Add Device</DropdownItem>
              <DropdownItem divider />
              <DropdownItem>Reset</DropdownItem>
            </DropdownMenu>
          </UncontrolledDropdown>
        </Nav>
        <UserButton />
      </Collapse>

      <Modal isOpen={modalOpen} toggle={toggleModal} size="lg">
        <ModalHeader toggle={toggleModal} style={{ backgroundColor: "white", borderBottom: "none" }}>Add House</ModalHeader>
        <ModalBody  style={{ backgroundColor: "white",}}>
          <div  style={{minWidth: '100px', height: '100%', overflowY: "auto" }}>
          <FormProvider />
          </div>
        </ModalBody>
      </Modal>
    </Navbar>
  );
};

export default Header;
