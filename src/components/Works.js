import { useState, useEffect } from 'react';
import Spinner from 'react-bootstrap/Spinner';
import { useApi } from '../contexts/ApiProvider';
import Work from './Work';
import More from './More';

export default function Works({ content }) {
  const [works, setWorks] = useState();
  const [pagination, setPagination] = useState();
  const api = useApi();

  let url;
  switch (content) {
    case 'feed':
    case 'undefined':
      url = '/prompters/1/feed';
      break;
    case 'explore':
      url = '/works';
      break;
    case 'liked':
      url = '/prompters/1/liked';
      break;
    default:
      url = `/prompters/${content}/works`;
      break;
  }

  useEffect(() => {
    (async () => {
      const response = await api.get(url);
      console.log(response);
      if (response.ok) {
        setWorks(response.body.items);
        setPagination(response.body._links);
      } else {
        setWorks(null);
      }
    })();
  }, [api, url]);

  const loadNextPage = async () => {
    const next = pagination.next.substring(4);
    const response = await api.get(next);
    if (response.ok) {
      setWorks([...works, ...response.body.items]);
      setPagination(response.body._links);
    }
  }

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
              <More pagination={pagination} loadNextPage={loadNextPage} />
            </>
          }
        </>
      }
    </>
  );
}