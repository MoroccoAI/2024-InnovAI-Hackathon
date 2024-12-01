interface Props {
    textContent: string;
    handleClick: () => void;
    // optional logic to disable the button
    disabled?: boolean;
  }
  
  const Button = ({ textContent, handleClick, disabled }: Props) => {
    return (
      <button type="submit" onClick={handleClick} disabled={disabled}>
        {textContent}
      </button>
    );
  };
  
  export default Button;