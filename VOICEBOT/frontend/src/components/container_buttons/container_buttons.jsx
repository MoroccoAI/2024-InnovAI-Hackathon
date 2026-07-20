import "./container_buttons.css";

export default function ButtonContainer({ activeContainer, setActiveContainer, name }) {
    return (
        <button className={activeContainer ? "active" : ""} onClick={() => setActiveContainer(name)}>
            {name}
        </button>
    );
}
