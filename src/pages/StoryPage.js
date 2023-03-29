import { useState, useEffect } from 'react';
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import Spinner from 'react-bootstrap/Spinner';
import { useParams, Link } from 'react-router-dom';
import Body from '../components/Body';
import TimeAgo from '../components/TimeAgo';
import { useApi } from '../contexts/ApiProvider';

export default function StoryPage() {
    const { id } = useParams();
    const [story, setStory] = useState();
    const api = useApi();

    useEffect(() => {
        (async () => {
            const response = await api.get('/stories/' + id);
            setStory(response.ok ? response.body : null);
        })();
    }, [id, api]);

    return (
        <Body sidebar>
            {story === undefined ?
                <Spinner animation="border" />
            :
                <>
                    {story === null ?
                        <p>Could not retrieve story.</p>
                    :
                        <>
                            <Stack direction="horizontal" gap={4}>
                                <Image src={story.prompter._links.avatar + '&s=128'} roundedCircle />
                                <div>
                                    <h1>{story.title}</h1>
                                    <h5>
                                        <Link to={'/prompter/' + story.prompter.id} className="prompter-link-header">
                                            {story.prompter.username}
                                        </Link>
                                    </h5>
                                    <p>
                                        Prompted: <TimeAgo isoDate={story.timestamp} />
                                    </p>
                                </div>
                            </Stack>
                            <p>{story.body}</p>
                        </>
                    }
                </>
            }
        </Body>
    );
}