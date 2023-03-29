import { useState, useEffect } from 'react';
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';
import Body from '../components/Body';
import TimeAgo from '../components/TimeAgo';
import { useApi } from '../contexts/ApiProvider';
import Works from '../components/Works';

export default function PrompterPage() {
    const { id } = useParams();
    const [prompter, setPrompter] = useState();
    const api = useApi();

    useEffect(() => {
        (async () => {
            const response = await api.get('/prompters/' + id);
            setPrompter(response.ok ? response.body : null);
        })();
    }, [id, api]);

    return (
        <Body sidebar>
            {prompter === undefined ?
                <Spinner animation="border" />
            :
                <>
                    {prompter === null ?
                        <p>Could not retrieve prompter works.</p>
                    :
                        <>
                            <Stack direction="horizontal" gap={4}>
                                <Image src={prompter._links.avatar + '&s=128'} roundedCircle />
                                <div>
                                    <h1>{prompter.username}</h1>
                                    {prompter.about_me && <h5>{prompter.about_me}</h5>}
                                    <p>
                                        Last seen: <TimeAgo isoDate={prompter.last_seen} />
                                    </p>
                                </div>
                            </Stack>
                            <Works content={id} />
                        </>
                    }
                </>
            }
        </Body>
    );
}