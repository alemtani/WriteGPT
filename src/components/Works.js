import { useState, useEffect } from 'react';
import Spinner from 'react-bootstrap/Spinner';
import Work from './Work';

export default function Works() {
  const [works, setWorks] = useState();

  useEffect(() => {
    (async () => {
      const response = await fetch('/api/prompters/1/feed');
      console.log(response);
      if (response.ok) {
        const results = await response.json();
        setWorks(results.items);
      } else {
        setWorks(null);
      }
    })();
  }, []);

  return (
    <>
      {works === undefined ?
        <Spinner animation="border" />
      :
        <>
          {works === null ?
            <p>Could not retrieve works.</p>
          :
            <>
              {works.length === 0 ?
                <p>There are no works to display.</p>
              :
                works.map(work => <Work key={work.id} work={work} />)
              }
            </>
          }
        </>
      }
    </>
  );
}