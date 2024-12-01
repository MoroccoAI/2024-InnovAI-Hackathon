import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import React from 'react'

function EndScreen({data,stepCount}) {
    const route=useRouter();
  return (
    <div>
          {data?.length==stepCount&&<div className='flex items-center gap-10 flex-col justify-center'>

                <h2>End of Notes</h2>
                <Button onClick={()=>route.back()}>Go to Course Page</Button>
            </div>}
    </div>
  )
}

export default EndScreen