import { useState, useEffect } from 'react';
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';
import Body from '../components/Body';
import TimeAgo from '../components/TimeAgo';
import { useApi } from '../contexts/ApiProvider';
import Stories from '../components/Stories';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserProvider';
import { useFlash } from '../contexts/FlashProvider';

export default function PrompterPage() {
    const { id } = useParams();
    const [prompter, setPrompter] = useState();
    const api = useApi();
    const [isFollower, setIsFollower] = useState();
    const { user } = useUser();
    const flash = useFlash();
    const navigate = useNavigate();

    useEffect(() => {
        (async () => {
            const response = await api.get('/prompters/' + id);
            if (response.ok) {
                setPrompter(response.body);
                if (response.body.username !== user.username) {
                    const follower = await api.get(`/prompters/${user.id}/following/${id}`);
                    const { isFollowing } = follower.body;
                    setIsFollower(isFollowing);
                } else {
                    setIsFollower(null);
                }
            } else {
                setPrompter(null);
            }
        })();
    }, [id, api, user]);

    const edit = () => {
        navigate('/edit');
    };

    const follow = async () => {
        const response = await api.post(`/prompters/${user.id}/following/${id}`);
        if (response.ok) {
            flash(
                <>
                    You are now following <b>{prompter.username}</b>.
                </>, 'success'
            );
            setIsFollower(true);
        }
    };

    const unfollow = async () => {
        const response = await api.delete(`/prompters/${user.id}/following/${id}`);
        if (response.ok) {
            flash(
                <>
                    You have unfollowed <b>{prompter.username}</b>.
                </>, 'success'
            );
            setIsFollower(false);
        }
    };

    return (
        <Body sidebar>
            {prompter === undefined ?
                <Spinner animation="border" />
            :
                <>
                    {prompter === null ?
                        <p>Prompter not found.</p>
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
                                    {isFollower === null &&
                                        <Button variant="primary" onClick={edit}>
                                            Edit
                                        </Button>
                                    }
                                    {isFollower === false &&
                                        <Button variant="primary" onClick={follow}>
                                            Follow
                                        </Button>
                                    }
                                    {isFollower === true &&
                                        <Button variant="primary" onClick={unfollow}>
                                            Unfollow
                                        </Button>
                                    }
                                </div>
                            </Stack>
                            <Stories content={id} />
                        </>
                    }
                </>
            }
        </Body>
    );
}