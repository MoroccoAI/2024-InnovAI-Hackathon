import './box.css';

export default function Box({title, onClick}) {
    return (
        <div className="card no-underline" onClick={onClick}>
            <p className="title">{title}</p>
            <p className="description">{title}</p>
        </div>
    );
}