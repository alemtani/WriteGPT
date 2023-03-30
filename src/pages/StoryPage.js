import { useState, useEffect } from 'react';
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import Spinner from 'react-bootstrap/Spinner';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Body from '../components/Body';
import TimeAgo from '../components/TimeAgo';
import { useApi } from '../contexts/ApiProvider';
import Button from 'react-bootstrap/Button';
import { useUser } from '../contexts/UserProvider';
import { useFlash } from '../contexts/FlashProvider';

export default function StoryPage() {
    const { id } = useParams();
    const [story, setStory] = useState();
    const api = useApi();
    const [isLiker, setIsLiker] = useState();
    const { user } = useUser();
    const flash = useFlash();
    const navigate = useNavigate();

    useEffect(() => {
        (async () => {
            const response = await api.get('/stories/' + id);
            if (response.ok) {
                setStory(response.body);
                const liker = await api.get(`/prompters/${user.id}/liking/${id}`);
                const { isLiking } = liker.body;
                setIsLiker(isLiking);
            } else {
                setStory(null);
            }
        })();
    }, [id, api, user]);

    const edit = () => {
        navigate(`/story/${id}/edit`);
    };

    const unwrite = async () => {
        const response = await api.delete(`/stories/${id}`);
        if (response.ok) {
            flash(
                <>
                    Successfully deleted <b>{story.title}</b>.
                </>, 'success'
            );
            navigate('/');
        }
    }

    const like = async () => {
        const response = await api.post(`/prompters/${user.id}/liking/${id}`);
        if (response.ok) {
            flash(
                <>
                    You are now liking <b>{story.title}</b>.
                </>, 'success'
            );
            setIsLiker(true);
        }
    };

    const unlike = async () => {
        const response = await api.delete(`/prompters/${user.id}/liking/${id}`);
        if (response.ok) {
            flash(
                <>
                    You have unliked <b>{story.title}</b>.
                </>, 'success'
            );
            setIsLiker(false);
        }
    };

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
                                    <Stack direction="horizontal" gap={2}>
                                        {isLiker === false &&
                                            <Button variant="primary" onClick={like}>
                                                Like
                                            </Button>
                                        }
                                        {isLiker === true &&
                                            <Button variant="primary" onClick={unlike}>
                                                Unlike
                                            </Button>
                                        }
                                        {story.prompter.id === user.id &&
                                            <>
                                                <Button variant="warning" onClick={edit}>
                                                    Edit
                                                </Button>
                                                <Button variant="danger" onClick={unwrite}>
                                                    Delete
                                                </Button>
                                            </>
                                        }
                                    </Stack>
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