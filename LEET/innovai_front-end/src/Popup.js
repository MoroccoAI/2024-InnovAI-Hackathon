import React from "react";

function Popup({ children, onClose }) {
    return (
        <div className="fixed inset-y-12 inset-x-32 flex items-center justify-center bg-white rounded-xl text-justify p-32" style={{ boxShadow: "rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px" }}>
            <div className="text-base font-medium leading-8 text-gray-800">{children}</div>
            <button className="btn text-red-500 absolute top-3 left-3 rounded-xl" onClick={onClose}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    className="size-6"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M6 18 18 6M6 6l12 12"
                    />
                </svg>
            </button>
        </div>
    );
}

export default Popup;
