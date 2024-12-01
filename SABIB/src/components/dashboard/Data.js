import React from 'react'
import { useDetails } from '../../hooks/details';



function Data() {
  const { details, error } = useDetails();
  return (
    <div>
      <h2>Clerck with firebase</h2>
      <div >
{
        details.map(({favorite_drink, favorite_food}) => {
            return (
              <div key={favorite_drink + favorite_food}>
                <h3>{favorite_drink}</h3>
                <p>{favorite_food}</p>
              </div>
            )
          })
}
      </div>
    </div>
  )
}
export default Data