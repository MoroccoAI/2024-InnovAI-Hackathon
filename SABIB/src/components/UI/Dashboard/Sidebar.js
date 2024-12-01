// import { Button, Nav, NavItem } from "reactstrap";
// import Logo from "./Logo";
// import { Link, useLocation } from "react-router-dom";

// const navigation = [
//   {
//     title: "Dashboard",
//     href: "starter",
//     icon: "bi bi-speedometer2",
//   },
//   {
//     title: "Alert",
//     href: "alerts",
//     icon: "bi bi-bell",
//   },
//   {
//     title: "Badges",
//     href: "badges",
//     icon: "bi bi-patch-check",
//   },
//   {
//     title: "Buttons",
//     href: "buttons",
//     icon: "bi bi-hdd-stack",
//   },
//   {
//     title: "Cards",
//     href: "cards",
//     icon: "bi bi-card-text",
//   },
//   {
//     title: "Grid",
//     href: "grid",
//     icon: "bi bi-columns",
//   },
//   {
//     title: "Table",
//     href: "table",
//     icon: "bi bi-layout-split",
//   },
//   {
//     title: "Forms",
//     href: "forms",
//     icon: "bi bi-textarea-resize",
//   },
//   {
//     title: "Breadcrumbs",
//     href: "breadcrumbs",
//     icon: "bi bi-link",
//   },
//   {
//     title: "About",
//     href: "about",
//     icon: "bi bi-people",
//   },
// ];

// const Sidebar = () => {
//   const showMobilemenu = () => {
//     document.getElementById("sidebarArea").classList.toggle("showSidebar");
//   };
//   let location = useLocation();

//   return (
//     <div className="p-3">
//       <div className="d-flex align-items-center">
//         <Logo />
//         <span className="ms-auto d-lg-none">
//         <Button
//           close
//           size="sm"
//           className="ms-auto d-lg-none"
//           onClick={() => showMobilemenu()}
//         ></Button>
//         </span>
//       </div>
//       <div className="pt-4 mt-2">
//         <Nav vertical className="sidebarNav">
//           {navigation.map((navi, index) => (
//             <NavItem key={index} className="sidenav-bg">
//               <Link
//                 to={navi.href}
//                 className={
//                   location.pathname === navi.href
//                     ? "text-primary nav-link py-3"
//                     : "nav-link text-secondary py-3"
//                 }
//               >
//                 <i className={navi.icon}></i>
//                 <span className="ms-3 d-inline-block">{navi.title}</span>
//               </Link>
//             </NavItem>
//           ))}
//         </Nav>
//       </div>
//     </div>
//   );
// };

// export default Sidebar;
import React from "react";
import { Button, Nav, NavItem } from "reactstrap";
import Logo from "./Logo";
import { Link, useLocation } from "react-router-dom";

const navigation = [
  {
    title: "Dashboard",
    href: "starter",
    icon: "bi bi-speedometer2",
  },
  {
    title: "Water Usage",
    href: "water-usage",
    icon: "bi bi-droplet",
  },
  {
    title: "Leak Detection",
    href: "alerts",
    icon: "bi bi-exclamation-triangle",
  },
  {
    title: "Flow Analytics",
    href: "flow-analytics",
    icon: "bi bi-bar-chart-line",
  },
  {
    title: "Alerts & Events",
    href: "table",
    icon: "bi bi-bell",
  },
  {
    title: "Settings",
    href: "settings",
    icon: "bi bi-gear",
  },
];

const Sidebar = () => {
  const showMobilemenu = () => {
    document.getElementById("sidebarArea").classList.toggle("showSidebar");
  };
  let location = useLocation();

  return (
    <div className="p-3">
      <div className="d-flex align-items-center">
        <Logo />
        <span className="ms-auto d-lg-none">
          <Button
            close
            size="sm"
            className="ms-auto d-lg-none"
            onClick={() => showMobilemenu()}
          ></Button>
        </span>
      </div>
      <div className="pt-4 mt-2">
        <Nav vertical className="sidebarNav">
          {navigation.map((navi, index) => (
            <NavItem key={index} className="sidenav-bg">
              <Link
                to={navi.href}
                className={
                  location.pathname === `/${navi.href}`
                    ? "text-primary nav-link py-3"
                    : "nav-link text-secondary py-3"
                }
              >
                <i className={navi.icon}></i>
                <span className="ms-3 d-inline-block">{navi.title}</span>
              </Link>
            </NavItem>
          ))}
        </Nav>
      </div>
    </div>
  );
};

export default Sidebar;
