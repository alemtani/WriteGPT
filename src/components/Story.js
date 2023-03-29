import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import { Link } from 'react-router-dom';
import TimeAgo from './TimeAgo';

export default function Story({ story }) {
    return (
        <Stack direction="horizontal" gap={3} className="Story">
            <Image src={story.prompter._links.avatar + '&s=48'} alt={story.prompter.username} roundedCircle />
            <div>
                <p>
                    <Link to={'/story/' + story.id}>
                        {story.title}
                    </Link>
                </p>
                <p>
                    <Link to={'/prompter/' + story.prompter.id} className="prompter-link">
                        {story.prompter.username}
                    </Link>
                    &nbsp;&mdash;&nbsp;
                    <TimeAgo isoDate={story.timestamp} />
                </p>
                <p>{story.body}</p>
            </div>
        </Stack>
    )
}