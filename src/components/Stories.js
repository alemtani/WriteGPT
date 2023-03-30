import { useState, useEffect } from 'react';
import Spinner from 'react-bootstrap/Spinner';
import { useApi } from '../contexts/ApiProvider';
import { useUser } from '../contexts/UserProvider';
import Story from './Story';
import More from './More';

export default function Stories({ content }) {
  const [stories, setStories] = useState();
  const [pagination, setPagination] = useState();
  const api = useApi();
  const { user } = useUser();

  let url;
  switch (content) {
    case 'feed':
    case 'undefined':
      url = `/prompters/${user.id}/feed`;
      break;
    case 'explore':
      url = '/stories';
      break;
    case 'liked':
      url = `/prompters/${user.id}/liking`;
      break;
    default:
      url = `/prompters/${content}/stories`;
      break;
  }

  useEffect(() => {
    (async () => {
      const response = await api.get(url);
      console.log(response);
      if (response.ok) {
        setStories(response.body.items);
        setPagination(response.body._links);
      } else {
        setStories(null);
      }
    })();
  }, [api, url]);

  const loadNextPage = async () => {
    const next = pagination.next.substring(4);
    const response = await api.get(next);
    if (response.ok) {
      setStories([...stories, ...response.body.items]);
      setPagination(response.body._links);
    }
  }

  return (
    <>
      {stories === undefined ?
        <Spinner animation="border" />
      :
        <>
          {stories === null ?
            <p>Could not retrieve stories.</p>
          :
            <>
              {stories.length === 0 ?
                <p>There are no stories to display.</p>
              :
                stories.map(story => <Story key={story.id} story={story} />)
              }
              <More pagination={pagination} loadNextPage={loadNextPage} />
            </>
          }
        </>
      }
    </>
  );
}